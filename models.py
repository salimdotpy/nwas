from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), nullable=False)
    email = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), nullable=False, unique=True)
    mobile = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    image = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    password = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'mobile': self.mobile,
            'image': self.image,
            'password': self.password,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

class Setting(db.Model):
    __tablename__ = "settings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_keys = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), nullable=False)
    data_values = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now)

    def to_dict(self):
        return {
            'id':self.id,
            'data_keys': self.data_keys,
            'data_values': eval(str(self.data_values)),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    role = db.Column(db.Boolean, nullable=False, default=0, comment='0: Security, 1: Coordinator')
    surname = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    othername = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    mobile = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    community = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    password = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), nullable=False)
    image = db.Column(db.String(255, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'surname': self.surname,
            'othername': self.othername,
            'mobile': self.mobile,
            'community': self.community,
            'password': self.password,
            'image': self.image,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }
        
class Incident(db.Model):
    __tablename__ = "incidents"

    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    uid = db.Column(db.BigInteger(), db.ForeignKey('users.id'), nullable=True)
    incident = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    community = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    status = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    remark = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    raiser = db.relationship('User', foreign_keys=uid)
    location = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now)
        
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    uid = db.Column(db.BigInteger(), db.ForeignKey('users.id'), nullable=True)
    text = db.Column(db.Text(collation='utf8mb4_unicode_ci'), nullable=False)
    community = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    status = db.Column(db.String(40, collation='utf8mb4_unicode_ci'), default=None, nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.now)