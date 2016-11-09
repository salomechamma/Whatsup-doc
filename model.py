"""Models and database functions for What's up Doc project."""

from flask_sqlalchemy import SQLAlchemy


# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of What's up doc website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s first_name=%s last_name=%s email=%s>" % (self.user_id,
                self.first_name, self.last_name, self.email)


class Doctor(db.Model):
    """US Doctors from Government Website."""

    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    yelp_rating = db.Column(db.Float, nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Doctor doctor_id=%s first_name=%s last_name=%s specialty=%s>"
        return s % (self.doctor_id, self.first_name, self.last_name,
                    self.specialty)

class Like(db.Model):
    """Doctor Likes per user."""

    __tablename__ = "likes"

    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False,)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Rating like_id=%s doctor_id=%s user_id=%s>"
        return s % (self.like_id, self.doctor_id, self.user_id)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("likes"))

    # Define relationship to movie
    doctor = db.relationship("Doctor",
                            backref=db.backref("likes"))
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///doctors'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
