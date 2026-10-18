from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True, cascade='all, delete-orphan')
    user_repairs = db.relationship('UserRepair', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    engine = db.Column(db.String(100), nullable=False)
    vin = db.Column(db.String(50), nullable=True)
    mileage = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user_repairs = db.relationship('UserRepair', backref='vehicle', lazy=True, cascade='all, delete-orphan')

    @property
    def display_name(self):
        return f"{self.year} {self.brand} {self.model} ({self.engine})"

    def __repr__(self):
        return f'<Vehicle {self.brand} {self.model} ({self.year})>'


class Repair(db.Model):
    __tablename__ = 'repairs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True) # Maintenance, Brakes, Electrical, Engine, Tires
    difficulty = db.Column(db.String(50), nullable=False) # Beginner, Intermediate, Advanced
    estimated_minutes = db.Column(db.Integer, nullable=False) # e.g. 30, 45, 60
    description = db.Column(db.Text, nullable=False)
    required_tools = db.Column(db.Text, nullable=False) # Comma-separated or newline-separated
    safety_warning = db.Column(db.Text, nullable=False)

    # Relationships
    steps = db.relationship('RepairStep', backref='repair', lazy=True, order_by='RepairStep.step_number', cascade='all, delete-orphan')
    user_repairs = db.relationship('UserRepair', backref='repair', lazy=True)

    @property
    def tools_list(self):
        if not self.required_tools:
            return []
        # Support both comma-separated and newline-separated
        tools = [t.strip() for t in self.required_tools.replace('\n', ',').split(',') if t.strip()]
        return tools

    @property
    def total_steps(self):
        return len(self.steps)

    def __repr__(self):
        return f'<Repair {self.title}>'


class RepairStep(db.Model):
    __tablename__ = 'repair_steps'

    id = db.Column(db.Integer, primary_key=True)
    repair_id = db.Column(db.Integer, db.ForeignKey('repairs.id', ondelete='CASCADE'), nullable=False, index=True)
    step_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    warning = db.Column(db.Text, nullable=True)

    __table_args__ = (
        db.UniqueConstraint('repair_id', 'step_number', name='uq_repair_step_number'),
    )

    def __repr__(self):
        return f'<RepairStep {self.repair_id} - Step {self.step_number}>'


class UserRepair(db.Model):
    __tablename__ = 'user_repairs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'), nullable=False, index=True)
    repair_id = db.Column(db.Integer, db.ForeignKey('repairs.id', ondelete='CASCADE'), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='IN_PROGRESS') # 'IN_PROGRESS' or 'COMPLETED'
    current_step = db.Column(db.Integer, nullable=False, default=1)
    notes = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    @property
    def progress_percentage(self):
        total = self.repair.total_steps if self.repair else 1
        if total == 0:
            return 100 if self.status == 'COMPLETED' else 0
        if self.status == 'COMPLETED':
            return 100
        # Progress based on current step
        pct = int(((self.current_step - 1) / total) * 100)
        return max(0, min(100, pct))

    def __repr__(self):
        return f'<UserRepair user={self.user_id} repair={self.repair_id} status={self.status}>'
