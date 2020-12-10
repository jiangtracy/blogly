from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DFLT_USR_IMG = 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg'


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User class """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    pic_url = db.Column(db.Text,
                        nullable=False,
                        default=DFLT_USR_IMG)

    @property
    def full_name(self):
        """ returns full name of user """

        return f"{self.first_name} {self.last_name}"

    posts = db.relationship('Post', backref='users')


class Post(db.Model):
    """ User class """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))

