from marshmallow import Schema, fields
import datetime
from . import db, bcrypt
from .BlogpostModel import BlogpostSchema

class UserModel(db.Model):
    """
    User Model

    """

    # Table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    blogposts = db.relationship('BlogpostModel', backref='users', lazy=True)

    # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()



    def generate_hash(self, password):
        """
        Generate password hash
        """
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    def check_hash(self, password):
        """
        Check password hash
        """
        return bcrypt.check_password_hash(self.password, password)
    

    def save(self):
        """
        Save to database
        """
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """
        Update to database
        """
        for key, item in data.items():
            if key=='password':
                self.password = self.generate_hash(item)
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        """
        Delete from database
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        """
        Get all users
        """
        return UserModel.query.all()
    
    @staticmethod
    def get_one_user(id):
        """
        Get one user
        """
        return UserModel.query.get(id)
    

    @staticmethod
    def get_user_by_email(email):
        """
        Get user by email
        """
        return UserModel.query.filter_by(email=email).first()
    
    def __repr(self):
        return '<id {}>'.format(self.id)
    

class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    blogposts = fields.Nested(BlogpostSchema, many=True)