import os
import unittest
import requests
from config import basedir
from app import app, db
from app.models import User
from unittest import TestCase
from unittest.mock import patch


class TestCase(TestCase):

    """
    Class allowing us to setting up our testing
    it is creating a test database
    """
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    """
    
    """
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('requests.post')
    def test_user_creation(self):
        """
        We check with this function that the user_creation works well
        We create an user in our testing database
        The tests we run are :
        - That there is one and only one user in the database
        - That each field of the user are correct in the database
        - That the hashing of the password is correct (returns false when a wrong password is typed in)
        :return: void
        """
        user = User(username='Username', email='test@test.co', name='Name', surname='Surname')
        user.set_password('Password')
        db.session.add(user)
        db.session.commit()
        u_all = User.query.all()
        u = User.query.filter_by(name='Name')
        assert len(u_all) == 1
        assert u.count() == 1
        assert u[0].username == 'Username'
        assert u[0].email == 'test@test.co'
        assert u[0].surname == 'Surname'
        assert u[0].check_password('Password')
        assert not u[0].check_password('Password' + 'x')

    def register(self, username, name, surname, email, password):
        return self.app.post('/register', data=dict(
            username=username,
            name=name,
            surname=surname,
            email=email,
            email2=email,
            password=password,
            password2=password
        ), follow_redirects=True)

    def test_user_registration(self):
        rv = TestCase.register(self, 'Username2',  'Name2', 'Surname2', 'test2@test.co', 'password2')
        assert b'Congratulations, you are now a registered user!' in rv.data


if __name__ == '__main__':
    unittest.main()



# @pytest.fixture
# def client():
#     db_fd, app.config['DATABASE'] = tempfile.mkstemp()
#     app.config['TESTING'] = True
#
#     with app.test_client() as client:
#         with app.app_context():
#             g.db = sqlite3.connect(
#                 current_app.config['DATABASE'],
#                 detect_types=sqlite3.PARSE_DECLTYPES
#             )
#             g.db.row_factory = sqlite3.Row
#         yield client
#
#     os.close(db_fd)
#     os.unlink(app.config['DATABASE'])
#
#
# def login(client, username, password):
#     return client.post('/login', data=dict(
#         username=username,
#         password=password
#     ), follow_redirects=True)
#
#
# def logout(client):
#     return client.get('/logout', follow_redirects=True)
#
#
# def test_login_logout(client):
#     """Make sure login and logout works."""
#     user = User(username='Username', email='test@test.co', name='Name', surname='Surname')
#     user.set_password('Password')
#     db.session.add(user)
#     db.session.commit()
#
#     rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
#     assert b'You were logged in' in rv.data
#
#     rv = logout(client)
#     assert b'You were logged out' in rv.data
#
#     rv = login(client, app.config['USERNAME'] + 'x', app.config['PASSWORD'])
#     assert b'Invalid username' in rv.data
#
#     rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'x')
#     assert b'Invalid password' in rv.data
#
