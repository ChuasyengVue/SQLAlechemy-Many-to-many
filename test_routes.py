from unittest import TestCase
from app import app
from models import db, User


class TestAppRoute(TestCase):
    """Test route in app"""

    def setup(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_show_user(self):
        with app.test_route() as route:
            response = route.get('/')
            self.assertEqual(response.status_code,302)
    
    def test_users_listing(self):
        with app.test_route() as route:
            response = route.get('/users')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Show lists of all users', response.data)



    
    def test_show_post_form(self):
        with app.test_route() as route:
            response = route.get('"/users/<int:user_id>/posts/new"')
            self.assertEqual(response.status_code, 200)