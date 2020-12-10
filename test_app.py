from unittest import TestCase
from app import app

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
            response = client.get('/users/<int:user_id>')

            # test that you're getting a template
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form action="/users/{{ user_id }}/edit"', html)
