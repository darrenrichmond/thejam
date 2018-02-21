from app import app, db
from app.models import User, Venue, Event

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Venue': Venue, 'Event': Event}