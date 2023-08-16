from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from microblog import login
from microblog import db


@login.user_loader
def load_user(id):
    """Loads the user ID for login session."""
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """Defines a class User."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True,
                         nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        """String representantion of User class."""
        return ("<{}: (id={}, username='{}', email='{}')>"
                .format(self.__class__.__name__,
                        self.id, self.username,
                        self.email)
                )

    def set_password(self, password):
        """Sets the password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Validates the password."""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Gets a user's profile picture."""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Post(db.Model):
    """Defines a class Post."""
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        """String representantion of Post class."""
        return ("<{}: (id={}, timestamp='{}', user_id={})>"
                .format(self.__class__.__name__,
                        self.id,
                        self.timestamp,
                        self.user_id)
                )
