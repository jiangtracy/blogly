"""Seed file to make sample data for users db."""
from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add user
joel = User(first_name='Joel',
            last_name='Joel',
            pic_url='http://shorturl.at/adCL2')
jane = User(first_name='Jane',
            last_name="Smith",
            pic_url='http://shorturl.at/adCL2')
alan = User(first_name='Alan',
            last_name="Stone",
            pic_url='http://shorturl.at/adCL2')

# Add new objects to session, so they'll persist
db.session.add(joel)
db.session.add(jane)
db.session.add(alan)
# Commit--otherwise,
db.session.commit()