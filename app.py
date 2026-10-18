import os
from datetime import datetime
from flask import (
    Flask, render_template, redirect, url_for, flash, request, abort, jsonify
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db, User, Vehicle, Repair, RepairStep, UserRepair
from forms import (
    RegistrationForm, LoginForm, VehicleForm, ProfileForm,
    StartRepairForm, RepairNoteForm
)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

csrf = CSRFProtect()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Context processor to inject current year or helpers
    @app.context_processor
    def inject_globals():
        return {
            'now_year': datetime.utcnow().year
        }

    # -------------------------------------------------------------
    # PUBLIC ROUTES
    # -------------------------------------------------------------

    @app.route('/')
    def index():
        featured_repairs = Repair.query.order_by(Repair.id.asc()).limit(4).all()
        return render_template('index.html', featured_repairs=featured_repairs)

    # -------------------------------------------------------------
    # AUTHENTICATION ROUTES
    # -------------------------------------------------------------

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(
                name=form.name.data.strip(),
                email=form.email.data.strip().lower()
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            # Log user in directly upon successful registration
            login_user(user)
            flash(f'Welcome to FixMyCar AI, {user.name}! Your account has been created.', 'success')
            return redirect(url_for('dashboard'))

        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.strip().lower()).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash(f'Welcome back, {user.name}!', 'success')
                next_page = request.args.get('next')
                # Ensure next_page is relative to prevent open-redirect vulnerabilities
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('dashboard')
                return redirect(next_page)
            else:
                flash('Invalid email or password. Please try again.', 'danger')

        return render_template('login.html', form=form)

    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        flash('You have been safely signed out.', 'info')
        return redirect(url_for('index'))

    # -------------------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------------------

    @app.route('/dashboard')
    @login_required
    def dashboard():
        vehicles = Vehicle.query.filter_by(user_id=current_user.id).order_by(Vehicle.created_at.desc()).all()
        repairs_in_progress = UserRepair.query.filter_by(
            user_id=current_user.id, status='IN_PROGRESS'
        ).order_by(UserRepair.started_at.desc()).all()
        
        recent_completed = UserRepair.query.filter_by(
            user_id=current_user.id, status='COMPLETED'
        ).order_by(UserRepair.completed_at.desc()).limit(5).all()

        guides = Repair.query.order_by(Repair.id.asc()).limit(6).all()

        return render_template(
            'dashboard.html',
            vehicles=vehicles,
            repairs_in_progress=repairs_in_progress,
            recent_completed=recent_completed,
            guides=guides
        )

    # -------------------------------------------------------------
    # GARAGE / VEHICLE MANAGEMENT
    # -------------------------------------------------------------

    @app.route('/garage')
    @login_required
    def garage():
        vehicles = Vehicle.query.filter_by(user_id=current_user.id).order_by(Vehicle.created_at.desc()).all()
        return render_template('garage.html', vehicles=vehicles)

    @app.route('/garage/add', methods=['GET', 'POST'])
    @login_required
    def add_vehicle():
        form = VehicleForm()
        if form.validate_on_submit():
            vehicle = Vehicle(
                user_id=current_user.id,
                brand=form.brand.data.strip(),
                model=form.model.data.strip(),
                year=form.year.data,
                engine=form.engine.data.strip(),
                vin=form.vin.data.strip() if form.vin.data else None,
                mileage=form.mileage.data if form.mileage.data else None
            )
            db.session.add(vehicle)
            db.session.commit()
            flash(f'Added {vehicle.display_name} to your garage!', 'success')
            return redirect(url_for('garage'))

        return render_template('add_vehicle.html', form=form, action_title='Add Vehicle')

    @app.route('/garage/<int:vehicle_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_vehicle(vehicle_id):
        vehicle = db.get_or_404(Vehicle, vehicle_id)
        # Enforce strict ownership check
        if vehicle.user_id != current_user.id:
            abort(403)

        form = VehicleForm(obj=vehicle)
        if form.validate_on_submit():
            vehicle.brand = form.brand.data.strip()
            vehicle.model = form.model.data.strip()
            vehicle.year = form.year.data
            vehicle.engine = form.engine.data.strip()
            vehicle.vin = form.vin.data.strip() if form.vin.data else None
            vehicle.mileage = form.mileage.data if form.mileage.data else None
            db.session.commit()
            flash(f'Updated {vehicle.display_name} successfully.', 'success')
            return redirect(url_for('garage'))

        return render_template('add_vehicle.html', form=form, action_title='Edit Vehicle', vehicle=vehicle)

    @app.route('/garage/<int:vehicle_id>/delete', methods=['POST'])
    @login_required
    def delete_vehicle(vehicle_id):
        vehicle = db.get_or_404(Vehicle, vehicle_id)
        # Enforce strict ownership check
        if vehicle.user_id != current_user.id:
            abort(403)

        vehicle_name = vehicle.display_name
        db.session.delete(vehicle)
        db.session.commit()
        flash(f'Removed {vehicle_name} from your garage.', 'info')
        return redirect(url_for('garage'))

    # -------------------------------------------------------------
    # REPAIR LIBRARY & DETAILS
    # -------------------------------------------------------------

    @app.route('/repairs')
    def repairs():
        category = request.args.get('category', '').strip()
        search_query = request.args.get('q', '').strip()

        query = Repair.query

        if category and category.lower() != 'all':
            query = query.filter(Repair.category.ilike(category))

        if search_query:
            query = query.filter(
                (Repair.title.ilike(f'%{search_query}%')) |
                (Repair.description.ilike(f'%{search_query}%'))
            )

        repair_list = query.order_by(Repair.id.asc()).all()

        categories = ['All', 'Maintenance', 'Brakes', 'Electrical', 'Engine', 'Tires']

        return render_template(
            'repairs.html',
            repairs=repair_list,
            categories=categories,
            current_category=category if category else 'All',
            search_query=search_query
        )

    @app.route('/repairs/<int:repair_id>')
    def repair_detail(repair_id):
        repair = db.get_or_404(Repair, repair_id)
        user_vehicles = []
        if current_user.is_authenticated:
            user_vehicles = Vehicle.query.filter_by(user_id=current_user.id).order_by(Vehicle.created_at.desc()).all()

        form = StartRepairForm()
        if user_vehicles:
            form.vehicle_id.choices = [(v.id, v.display_name) for v in user_vehicles]

        return render_template(
            'repair_detail.html',
            repair=repair,
            user_vehicles=user_vehicles,
            form=form
        )

    # -------------------------------------------------------------
    # REPAIR PROGRESS & ACTIVE SESSIONS
    # -------------------------------------------------------------

    @app.route('/repairs/<int:repair_id>/start', methods=['POST'])
    @login_required
    def start_repair(repair_id):
        repair = db.get_or_404(Repair, repair_id)
        user_vehicles = Vehicle.query.filter_by(user_id=current_user.id).all()

        if not user_vehicles:
            flash('Please add a vehicle to your garage before starting a repair session.', 'warning')
            return redirect(url_for('add_vehicle'))

        form = StartRepairForm()
        form.vehicle_id.choices = [(v.id, v.display_name) for v in user_vehicles]

        if form.validate_on_submit():
            vehicle_id = form.vehicle_id.data
            vehicle = db.get_or_404(Vehicle, vehicle_id)

            # Strict ownership verification
            if vehicle.user_id != current_user.id:
                abort(403)

            # Check if there is already an active in-progress session for this vehicle and repair
            existing_session = UserRepair.query.filter_by(
                user_id=current_user.id,
                vehicle_id=vehicle.id,
                repair_id=repair.id,
                status='IN_PROGRESS'
            ).first()

            if existing_session:
                flash(f'Resuming ongoing repair session for {vehicle.display_name}.', 'info')
                return redirect(url_for('repair_session', session_id=existing_session.id))

            # Create new user_repair record
            session_record = UserRepair(
                user_id=current_user.id,
                vehicle_id=vehicle.id,
                repair_id=repair.id,
                status='IN_PROGRESS',
                current_step=1,
                started_at=datetime.utcnow()
            )
            db.session.add(session_record)
            db.session.commit()

            flash(f'Started repair guide: {repair.title} on {vehicle.display_name}.', 'success')
            return redirect(url_for('repair_session', session_id=session_record.id))

        flash('Please select a valid vehicle from your garage.', 'danger')
        return redirect(url_for('repair_detail', repair_id=repair.id))

    @app.route('/repair-session/<int:session_id>', methods=['GET'])
    @login_required
    def repair_session(session_id):
        session_record = db.get_or_404(UserRepair, session_id)

        # Enforce strict ownership check
        if session_record.user_id != current_user.id:
            abort(403)

        repair = session_record.repair
        vehicle = session_record.vehicle
        steps = repair.steps
        total_steps = len(steps)

        # Ensure current_step is within valid range
        if session_record.current_step < 1:
            session_record.current_step = 1
            db.session.commit()
        elif total_steps > 0 and session_record.current_step > total_steps:
            session_record.current_step = total_steps
            db.session.commit()

        # Find current step object
        current_step_obj = None
        for step in steps:
            if step.step_number == session_record.current_step:
                current_step_obj = step
                break

        if not current_step_obj and steps:
            current_step_obj = steps[0]

        note_form = RepairNoteForm(notes=session_record.notes)

        return render_template(
            'repair_session.html',
            session_record=session_record,
            repair=repair,
            vehicle=vehicle,
            steps=steps,
            total_steps=total_steps,
            current_step=session_record.current_step,
            current_step_obj=current_step_obj,
            note_form=note_form
        )

    @app.route('/repair-session/<int:session_id>/step', methods=['POST'])
    @login_required
    def update_repair_step(session_id):
        session_record = db.get_or_404(UserRepair, session_id)
        if session_record.user_id != current_user.id:
            abort(403)

        target_step = request.form.get('target_step', type=int)
        direction = request.form.get('direction', '')

        total_steps = session_record.repair.total_steps

        if target_step is not None:
            new_step = max(1, min(total_steps, target_step))
        elif direction == 'next':
            new_step = min(total_steps, session_record.current_step + 1)
        elif direction == 'prev':
            new_step = max(1, session_record.current_step - 1)
        else:
            new_step = session_record.current_step

        session_record.current_step = new_step
        db.session.commit()

        # Check if requested via AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({
                'success': True,
                'current_step': session_record.current_step,
                'total_steps': total_steps,
                'progress_percentage': session_record.progress_percentage
            })

        return redirect(url_for('repair_session', session_id=session_record.id))

    @app.route('/repair-session/<int:session_id>/finish', methods=['POST'])
    @login_required
    def finish_repair_session(session_id):
        session_record = db.get_or_404(UserRepair, session_id)
        if session_record.user_id != current_user.id:
            abort(403)

        notes = request.form.get('notes', '').strip()
        session_record.notes = notes if notes else session_record.notes
        session_record.status = 'COMPLETED'
        session_record.completed_at = datetime.utcnow()
        session_record.current_step = session_record.repair.total_steps
        db.session.commit()

        flash(f'Congratulations! You successfully completed: {session_record.repair.title} on {session_record.vehicle.display_name}!', 'success')
        return redirect(url_for('my_repairs'))

    # -------------------------------------------------------------
    # REPAIR HISTORY
    # -------------------------------------------------------------

    @app.route('/my-repairs')
    @login_required
    def my_repairs():
        in_progress = UserRepair.query.filter_by(
            user_id=current_user.id, status='IN_PROGRESS'
        ).order_by(UserRepair.started_at.desc()).all()

        completed = UserRepair.query.filter_by(
            user_id=current_user.id, status='COMPLETED'
        ).order_by(UserRepair.completed_at.desc()).all()

        return render_template(
            'my_repairs.html',
            in_progress=in_progress,
            completed=completed
        )

    @app.route('/my-repairs/<int:session_id>/notes', methods=['POST'])
    @login_required
    def update_repair_notes(session_id):
        session_record = db.get_or_404(UserRepair, session_id)
        if session_record.user_id != current_user.id:
            abort(403)

        notes = request.form.get('notes', '').strip()
        session_record.notes = notes
        db.session.commit()

        flash('Repair notes updated successfully.', 'success')
        return redirect(url_for('my_repairs'))

    # -------------------------------------------------------------
    # PROFILE
    # -------------------------------------------------------------

    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm(obj=current_user)
        if form.validate_on_submit():
            current_user.name = form.name.data.strip()
            db.session.commit()
            flash('Your profile name has been updated.', 'success')
            return redirect(url_for('profile'))

        vehicles_count = Vehicle.query.filter_by(user_id=current_user.id).count()
        repairs_completed_count = UserRepair.query.filter_by(
            user_id=current_user.id, status='COMPLETED'
        ).count()

        return render_template(
            'profile.html',
            form=form,
            vehicles_count=vehicles_count,
            repairs_completed_count=repairs_completed_count
        )

    # -------------------------------------------------------------
    # ERROR HANDLERS
    # -------------------------------------------------------------

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('404.html', error_title='403 - Access Denied', error_message='You do not have permission to access or modify this resource.'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('404.html', error_title='500 - Server Error', error_message='An unexpected error occurred. Please try again shortly.'), 500

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
