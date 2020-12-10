from unittest import TestCase
from app import app
from models import db, connect_db, User
from flask import jsonify

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class ConversionAppTestCase(TestCase):
    """ Test flask app of blogly. """

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_users_list_page(self):
        """Make sure HTML is displayed"""

        with self.client as client:
            response = client.get('/users')

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('/users/new', html)

    def test_show_user_info(self):
        """ make sure user info page displays """

        with self.client as client:

            test_user = User.query.first()
            user_id = test_user.id
            response = client.get(f'/users/{user_id}')

            html = response.get_data(as_text=True)

            if test_user is None:
                self.assertEqual(response.status_code, 404)
            else:
                self.assertEqual(response.status_code, 200)
                self.assertIn('user_detail', html)

    def test_add_new_user(self):
        """ Test if new user is added to the database """

        post_body = {
            'first_name': 'Test8',
            'last_name': 'Test1',
            'pic_url': ''
            }

        with self.client as client:
            client.post("/users/new", data=post_body)

        self.assertTrue(User.query.filter(User.first_name == 'Test8'))

    def test_delete_user(self):
        """ Test deletion of user from database """

        user = User.query.filter(User.first_name == 'Test8').first()

        db.session.delete(user)
        db.session.commit()

        self.assertFalse(User.query.get(user.id))
