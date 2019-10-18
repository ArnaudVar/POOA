import os
import unittest

from classes.Exception import SetterException
from config import basedir
from app import app, db
from app.models import User
from unittest import TestCase
from classes.media import Media
from classes.episode import Episode
import logging


class TestApplication(TestCase):

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

    def register(self, username, name, surname, email1, email2, password1, password2):
        """
        This function is used to simulate a register event for a new user on our register page.
        We fill all the fields and check that the new user is allowed to register
        :param username: string
        :param name: string
        :param surname: string
        :param email: string
        :param password: string
        :return: void
        """
        return self.app.post('/register', data=dict(
            username=username,
            name=name,
            surname=surname,
            email=email1,
            email2=email2,
            password=password1,
            password2=password2
        ), follow_redirects=True)

    def test_user_registration(self):
        """
        This method allows us to check that the registration of the users takes place without problems
        We check that when a user registers, a successful message is flashed

        We also check that in the following cases the user is not created (errors message are flashed
        in the register page):
        - Username already taken
        - Email already taken
        - Email not in the good format (not in xxx@xxx.xx)
        - The two fields email aren't matching
        - The two password fields aren't matching
        :return: void
        """
        # We check that a user can register if all the correct info is typed in
        # To check if the registration took place correctly, we check the logs
        with self.assertLogs() as cm :
            TestApplication.register(self, 'Username2',  'Name2', 'Surname2', 'test2@test.co', 'test2@test.co',
                                          'password2', 'password2')
        self.assertEqual(cm.records[0].msg, 'Successful registry')

        #We check that a user can't register with the same username than an already existing user
        rv2 = TestApplication.register(self, 'Username2',  'Name3', 'Surname3', 'test3@test.co', 'test3@test.co',
                                       'password3', 'password3')
        assert b'This username is already used, please use a different username.' in rv2.data

        # We check that a user can't register with the same email than an already existing user
        rv3 = TestApplication.register(self, 'Username3', 'Name3', 'Surname3', 'test2@test.co', 'test2@test.co',
                                       'password3', 'password3')
        assert b'This e-mail is already used, please use a different email address.' in rv3.data

        # We check that the user must type in an email that matches the email format
        rv4 = TestApplication.register(self, 'Username3', 'Name3', 'Surname3', 'test3test.co', 'test3test.co',
                                       'password3', 'password3')
        assert b'Invalid email address.' in rv4.data

        # We check that a user can't register if the validation email isn't equal to the email first typed in
        rv5 = TestApplication.register(self, 'Username3', 'Name3', 'Surname3', 'test3@test.co', 'test3@test.com',
                                       'password3', 'password3')
        assert b'Field must be equal to email.' in rv5.data

        # We check that a user can't register if the validation password isn't equal to the password first typed in
        rv6 = TestApplication.register(self, 'Username3', 'Name3', 'Surname3', 'test3@test.co', 'test3@test.co',
                                       'password3', 'password3x')
        assert b'Field must be equal to password.' in rv6.data

    def login(self, username, password):
        """
        This function is used to simulate a login event for a user on our login page.
        We fill all the fields and check that the user is allowed to login
        :param username: string
        :param password: string
        :return: void
        """
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """
        Method allowing us to logout a user
        :return: void
        """
        return self.app.get('/logout', follow_redirects=True)

    def test_user_login_logout(self):
        """
        This method allows us to check that the login of the users takes place without problems
        We check that when a user logs in, a successful message is flashed

        We also check that a user can't login if he types in the wrong info (wrong username or wrong password)
        :return: void
        """
        # We check that a user can log in if all the correct info is typed in
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                     'password', 'password')
        with self.assertLogs() as cm:
            TestApplication.login(self, 'Username',  'password')
        self.assertEqual(cm.records[0].msg, 'Successful Login !')

        # We check that the logout is succesful
        with self.assertLogs() as cm:
            self.logout()
        self.assertEqual(cm.records[0].msg, 'Successful Logout !')

        # We check that a user can't log in if there is a mistake in its username
        with self.assertLogs() as cm:
            TestApplication.login(self, 'Username2', 'password')
        self.assertEqual(cm.records[0].msg, 'Invalid Username !')

        # We check that a user can't log in if there is a mistake in its password
        with self.assertLogs() as cm:
            TestApplication.login(self, 'Username', 'password2')
        self.assertEqual(cm.records[0].msg, 'Invalid Password !')

    # def test_routes_serie(self):


class TestMedia(TestCase):
    m = Media(name='Name', description='description', grade='grade', image='image')

    def test__get_name(self):
        self.assertEqual(TestMedia.m._get_name(), 'Name')

    def test__set_name(self):
        self.assertRaises(SetterException)

    def test__get_description(self):
        self.assertEqual(TestMedia.m._get_description(), 'description')

    def test__set_description(self):
        self.assertRaises(SetterException)

    def test__get_image(self):
        self.assertEqual(TestMedia.m._get_image(), 'image')

    def test__set_image(self):
        self.assertRaises(SetterException)


class TestEpisode(TestCase):
    ep = Episode(id='',  name='Arrow', description='description', cast='cast', grade='grade',
                 image='image', id_serie='1412', num_season='2', num_episode='3', release='release')
    def test__get_id_serie(self):
        self.assertEqual(TestEpisode.ep._get_id_serie(), '1412')

    def test__set_id_serie(self):
        self.assertRaises(SetterException)

    def test_id_episode(self):
        self.assertEqual(f'S{TestEpisode.ep.num_season}E{TestEpisode.ep.num_episode}', TestEpisode.ep._id)




if __name__ == '__main__':
    unittest.main()



