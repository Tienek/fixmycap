import re
import unittest
from app import create_app
from models import db, User, Vehicle, Repair, RepairStep, UserRepair
from config import Config

def extract_csrf(html_data):
    html = html_data.decode('utf-8')
    match = re.search(r'name=["\']csrf_token["\'][^>]*?value=["\']([^"\']+)["\']', html)
    if not match:
        match = re.search(r'value=["\']([^"\']+)["\'][^>]*?name=["\']csrf_token["\']', html)
    return match.group(1) if match else ''

class TestCSRFConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = True
    SERVER_NAME = 'localhost'

class EndToEndCSRFTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestCSRFConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        # Seed repairs
        from seed import SEED_REPAIRS
        for r_data in SEED_REPAIRS:
            repair = Repair(
                title=r_data["title"],
                slug=r_data["slug"],
                category=r_data["category"],
                difficulty=r_data["difficulty"],
                estimated_minutes=r_data["estimated_minutes"],
                description=r_data["description"],
                required_tools=r_data["required_tools"],
                safety_warning=r_data["safety_warning"]
            )
            db.session.add(repair)
            db.session.flush()
            for s_data in r_data["steps"]:
                step = RepairStep(
                    repair_id=repair.id,
                    step_number=s_data["step_number"],
                    title=s_data["title"],
                    description=s_data["description"],
                    warning=s_data.get("warning")
                )
                db.session.add(step)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_full_user_lifecycle_with_real_csrf(self):
        # 1. Landing Page
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"REPAIR YOUR CAR AT HOME.", r.data)

        # 2. Registration with CSRF
        reg_page = self.client.get('/register')
        csrf_token = extract_csrf(reg_page.data)
        self.assertTrue(bool(csrf_token), "CSRF token must be present on register page")

        r = self.client.post('/register', data={
            'csrf_token': csrf_token,
            'name': 'Test Pilot',
            'email': 'testpilot@example.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Welcome to FixMyCar AI, Test Pilot!", r.data)

        # 3. Add vehicle with CSRF
        add_page = self.client.get('/garage/add')
        csrf_token = extract_csrf(add_page.data)
        r = self.client.post('/garage/add', data={
            'csrf_token': csrf_token,
            'brand': 'Mazda',
            'model': 'Miata',
            'year': 2016,
            'engine': '2.0L SkyActiv-G',
            'vin': 'JM1NDAD79G1123456',
            'mileage': 38000
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Mazda Miata", r.data)

        # 4. Start Repair Session
        v = Vehicle.query.filter_by(brand='Mazda').first()
        rep = Repair.query.filter_by(slug='engine-oil-change').first()
        v_id = v.id
        rep_id = rep.id

        detail_page = self.client.get(f'/repairs/{rep_id}')
        csrf_token = extract_csrf(detail_page.data)
        r = self.client.post(f'/repairs/{rep_id}/start', data={
            'csrf_token': csrf_token,
            'vehicle_id': v_id
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Step 1 of 9", r.data)

        # 5. Advance to next step
        session_rec = UserRepair.query.filter_by(vehicle_id=v_id, repair_id=rep_id).first()
        session_id = session_rec.id

        session_page = self.client.get(f'/repair-session/{session_id}')
        csrf_token = extract_csrf(session_page.data)
        r = self.client.post(f'/repair-session/{session_id}/step', data={
            'csrf_token': csrf_token,
            'direction': 'next'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Step 2 of 9", r.data)

        # 6. Finish repair with notes
        session_page = self.client.get(f'/repair-session/{session_id}')
        csrf_token = extract_csrf(session_page.data)
        r = self.client.post(f'/repair-session/{session_id}/finish', data={
            'csrf_token': csrf_token,
            'notes': 'Replaced with 0W-20 Castrol and Mazda OEM filter. Checked crush washer.'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Congratulations!", r.data)
        self.assertIn(b"Mazda OEM filter", r.data)

        # 7. Update profile name
        prof_page = self.client.get('/profile')
        csrf_token = extract_csrf(prof_page.data)
        r = self.client.post('/profile', data={
            'csrf_token': csrf_token,
            'name': 'Captain Pilot'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"Captain Pilot", r.data)

        # 8. Logout
        csrf_token = extract_csrf(r.data)
        r = self.client.post('/logout', data={'csrf_token': csrf_token}, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"You have been safely signed out.", r.data)

if __name__ == '__main__':
    unittest.main()
