from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin

#Inherits from UserMixin in order to get standard implementations of the required Flask-Login methods
#Inherits from db.Model to work with the SQLAlchemy model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    home_address = db.Column(db.String(120), index=True)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(120))
    website = db.Column(db.String(128))

    def __repr__(self):
        return '<Venue {}>'.format(self.name)

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'address' : self.address,
            'website' : self.website
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    night = db.Column(db.String(10),index=True)
    recurs = db.Column(db.String(32))
    start_time = db.Column(db.String(8))
    end_time = db.Column(db.String(8))
    adv_signup = db.Column(db.String(8))
    notes = db.Column(db.String(128))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

    def __repr__(self):
        venue = Venue.query.get(self.venue_id)
        return '<Event {}>'.format(str(venue.name) + " " + self.night)

    def serialize(self):
            venue = Venue.query.get(self.venue_id)
            venue_ser = venue.serialize()
            return {
                'id' : self.id,
                'night' : self.night,
                'start_time' : self.start_time,
                'end_time' : self.end_time,
                'adv_signup' : self.adv_signup,
                'notes' : self.notes,
                'venue' : venue_ser,
            }

    def getAddress(self):
        venue = Venue.query.get(self.venue_id)
        address = venue.address
        return address      

@login.user_loader
def load_user(id):
    return User.query.get(int(id))