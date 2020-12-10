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

            # test that you're getting a template
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form action="/users/new">', html)

    def test_show_user_info(self):
        """ make sure user info page displays """

        with self.client as client:

            test_user = User.query.first()
            user_id = test_user.id
            response = client.get(f'/users/{user_id}')
      
            # test that you're getting a template
            html = response.get_data(as_text=True)

            if test_user == None:
                self.assertEqual(response.status_code, 404)
            else:
                self.assertEqual(response.status_code, 200)
                self.assertIn('user_detail', html)

    def test_add_new_user(self):
        """ Test if new user is added to the database """

        with self.client as client:
            user = client.post("/users/new", json={
                        'first_name': 'Test1',
                        'last_name': 'Test1',
                        'pic_url': None
                        })

        print(user)

        # new_user = User(first_name='Test',
        #                 last_name='Test1',
        #                 pic_url=None)

        # db.session.add(new_user)
        # db.session.commit()

        # self.assertTrue(User.query.filter(User.first_name == 'Test')) 

    # def test_delete_user(self):
    #     """ Test delete user """

    #     user = User.query.filter(User.first_name == 'Test').first()

    #     db.session.delete(user)
    #     db.session.commit()

    #     print('userrrrrrrrrrrrrrrrrrr', User.query.filter(User.first_name == 'Test').first())


    #     # self.assertFalse(User.query.filter(User.first_name == 'Test'))
