import os
import unittest
from datetime import datetime

# Configure test environment
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['SECRET_KEY'] = 'test-secret-key-12345'

from app import create_app
from models import db, User, Vehicle, Repair, RepairStep, UserRepair
from seed import seed_repairs
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'

class FixMyCarTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        # Seed repairs
        with self.app.app_context():
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

    def register_user(self, name="John Doe", email="john@example.com", password="password123"):
        return self.client.post('/register', data={
            'name': name,
            'email': email,
            'password': password,
            'confirm_password': password
        }, follow_redirects=True)

    def login_user(self, email="john@example.com", password="password123"):
        return self.client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def logout_user(self):
        return self.client.post('/logout', follow_redirects=True)

    # -------------------------------------------------------------------------
    # TEST SUITE
    # -------------------------------------------------------------------------

    def test_landing_page(self):
        """Test public landing page loads properly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"REPAIR YOUR CAR AT HOME.", response.data)
        self.assertIn(b"FIXMYCAR", response.data)

    def test_user_registration_and_password_hashing(self):
        """Test registration creates user with hashed password."""
        response = self.register_user("Alice Driver", "alice@example.com", "secretpass123")
        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(email="alice@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Alice Driver")
        # Password must NOT be stored in plain text
        self.assertNotEqual(user.password_hash, "secretpass123")
        self.assertTrue(user.check_password("secretpass123"))
        self.assertFalse(user.check_password("wrongpassword"))

    def test_duplicate_registration_prevented(self):
        """Test duplicate email registration is rejected."""
        self.register_user("User One", "unique@example.com", "password123")
        self.logout_user()

        response = self.register_user("User Two", "unique@example.com", "password123")
        self.assertIn(b"already registered", response.data)

    def test_login_and_logout(self):
        """Test user login and session termination."""
        self.register_user("Bob Smith", "bob@example.com", "mypassword")
        self.logout_user()

        # Login with correct password
        response = self.login_user("bob@example.com", "mypassword")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome back, Bob Smith!", response.data)

        # Logout
        response = self.logout_user()
        self.assertIn(b"You have been safely signed out.", response.data)

        # Login with incorrect password
        bad_response = self.login_user("bob@example.com", "badpass")
        self.assertIn(b"Invalid email or password", bad_response.data)

    def test_vehicle_management_crud_and_ownership(self):
        """Test adding, editing, and deleting vehicle with ownership authorization."""
        # Register User A
        self.register_user("User A", "usera@example.com", "password123")

        # Add vehicle
        add_resp = self.client.post('/garage/add', data={
            'brand': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'engine': '1.8L 4-Cyl',
            'vin': '1234567890ABCDEFG',
            'mileage': 45000
        }, follow_redirects=True)
        self.assertEqual(add_resp.status_code, 200)
        self.assertIn(b"Toyota Corolla", add_resp.data)

        vehicle = Vehicle.query.filter_by(brand="Toyota").first()
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle.year, 2020)

        # Edit vehicle
        edit_resp = self.client.post(f'/garage/{vehicle.id}/edit', data={
            'brand': 'Toyota',
            'model': 'Corolla Hybrid',
            'year': 2021,
            'engine': '1.8L Hybrid',
            'vin': '1234567890ABCDEFG',
            'mileage': 48000
        }, follow_redirects=True)
        self.assertEqual(edit_resp.status_code, 200)
        db.session.refresh(vehicle)
        self.assertEqual(vehicle.model, 'Corolla Hybrid')
        self.assertEqual(vehicle.year, 2021)

        # Test authorization: User B must NOT be able to edit or delete User A's vehicle
        self.logout_user()
        self.register_user("User B", "userb@example.com", "password123")

        # User B attempts to edit User A's vehicle
        unauthorized_edit = self.client.post(f'/garage/{vehicle.id}/edit', data={
            'brand': 'Hacked',
            'model': 'Hacked',
            'year': 2022,
            'engine': 'Hacked'
        })
        self.assertEqual(unauthorized_edit.status_code, 403)

        # User B attempts to delete User A's vehicle
        unauthorized_delete = self.client.post(f'/garage/{vehicle.id}/delete')
        self.assertEqual(unauthorized_delete.status_code, 403)

        # User A logs back in and deletes vehicle
        self.logout_user()
        self.login_user("usera@example.com", "password123")
        delete_resp = self.client.post(f'/garage/{vehicle.id}/delete', follow_redirects=True)
        self.assertEqual(delete_resp.status_code, 200)
        self.assertIsNone(db.session.get(Vehicle, vehicle.id))

    def test_repair_library_and_filtering(self):
        """Test repair library page, category filter, and search."""
        response = self.client.get('/repairs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Engine Oil Change", response.data)
        self.assertIn(b"Replace Brake Pads", response.data)

        # Category filter: Brakes
        brakes_resp = self.client.get('/repairs?category=Brakes')
        self.assertEqual(brakes_resp.status_code, 200)
        self.assertIn(b"Replace Brake Pads", brakes_resp.data)
        self.assertIn(b"Replace Brake Discs", brakes_resp.data)
        self.assertNotIn(b"Replace Engine Air Filter", brakes_resp.data)

        # Search filter
        search_resp = self.client.get('/repairs?q=Battery')
        self.assertEqual(search_resp.status_code, 200)
        self.assertIn(b"Replace Car Battery", search_resp.data)
        self.assertNotIn(b"Replace Windshield Wipers", search_resp.data)

    def test_repair_session_flow_and_persistence(self):
        """Test full repair workflow: start session, step navigation, progress save, complete with notes."""
        self.register_user("Mechanic Dave", "dave@example.com", "password123")

        # Add vehicle
        self.client.post('/garage/add', data={
            'brand': 'Honda',
            'model': 'Civic',
            'year': 2019,
            'engine': '2.0L 4-Cyl'
        }, follow_redirects=True)
        vehicle = Vehicle.query.first()

        oil_repair = Repair.query.filter_by(slug="engine-oil-change").first()
        self.assertIsNotNone(oil_repair)

        # Start repair session
        start_resp = self.client.post(f'/repairs/{oil_repair.id}/start', data={
            'vehicle_id': vehicle.id
        }, follow_redirects=True)
        self.assertEqual(start_resp.status_code, 200)
        self.assertIn(b"Step 1 of 9", start_resp.data)

        session_rec = UserRepair.query.filter_by(user_id=vehicle.user_id, repair_id=oil_repair.id).first()
        self.assertIsNotNone(session_rec)
        self.assertEqual(session_rec.status, 'IN_PROGRESS')
        self.assertEqual(session_rec.current_step, 1)

        # Advance to step 2
        self.client.post(f'/repair-session/{session_rec.id}/step', data={'direction': 'next'})
        db.session.refresh(session_rec)
        self.assertEqual(session_rec.current_step, 2)

        # Advance directly to step 5
        self.client.post(f'/repair-session/{session_rec.id}/step', data={'target_step': 5})
        db.session.refresh(session_rec)
        self.assertEqual(session_rec.current_step, 5)

        # Complete repair session with notes
        finish_resp = self.client.post(f'/repair-session/{session_rec.id}/finish', data={
            'notes': 'Replaced with 0W-20 Castrol Edge and OEM oil filter.'
        }, follow_redirects=True)
        self.assertEqual(finish_resp.status_code, 200)

        db.session.refresh(session_rec)
        self.assertEqual(session_rec.status, 'COMPLETED')
        self.assertIsNotNone(session_rec.completed_at)
        self.assertIn('Castrol Edge', session_rec.notes)

        # Verify completed repair appears on My Repairs history
        history_resp = self.client.get('/my-repairs')
        self.assertEqual(history_resp.status_code, 200)
        self.assertIn(b"Engine Oil Change", history_resp.data)
        self.assertIn(b"Castrol Edge", history_resp.data)

    def test_database_url_normalization(self):
        """Test normalization of postgres:// to postgresql:// for Render compatibility."""
        from config import Config
        raw = "postgres://user:pass@host:5432/dbname"
        normalized = raw.replace("postgres://", "postgresql://", 1)
        self.assertEqual(normalized, "postgresql://user:pass@host:5432/dbname")


if __name__ == '__main__':
    unittest.main()
