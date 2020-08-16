from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from sqlalchemy.sql import expression


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    is_active = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    is_superuser = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    can_review_tasks = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='creator')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lower_limit = db.Column(db.Float, nullable=False)
    upper_limit = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Task {}'.format(self.id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
