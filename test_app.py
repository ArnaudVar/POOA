import os
import unittest

from flask import url_for, g

from app.api import Api
from app.forms import SearchForm
from classes.Exception import SetterException
from config import basedir
from app import app, db
from app.models import User
from unittest import TestCase
from classes.media import Media
from classes.episode import Episode


# class TestApplication(TestCase):
#
#     """
#     Class allowing us to setting up our testing
#     it is creating a test database
#     """
#     def setUp(self):
#         app.config['TESTING'] = True
#         app.config['WTF_CSRF_ENABLED'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
#         self.app = app.test_client()
#         db.create_all()
#     #
#     # def test_user_creation(self):
#     #     """
#     #     We check with this function that the user_creation works well
#     #     We create an user in our testing database
#     #     The tests we run are :
#     #     - That there is one and only one user in the database
#     #     - That each field of the user are correct in the database
#     #     - That the hashing of the password is correct (returns false when a wrong password is typed in)
#     #     :return: void
#     #     """
#     #     user = User(username='Username', email='test@test.co', name='Name', surname='Surname')
#     #     user.set_password('Password')
#     #     db.session.add(user)
#     #     db.session.commit()
#     #     u_all = User.query.all()
#     #     u = User.query.filter_by(name='Name')
#     #     assert len(u_all) == 1
#     #     assert u.count() == 1
#     #     assert u[0].username == 'Username'
#     #     assert u[0].email == 'test@test.co'
#     #     assert u[0].surname == 'Surname'
#     #     assert u[0].check_password('Password')
#     #     assert not u[0].check_password('Password' + 'x')
#
#     def register(self, username, name, surname, email1, email2, password1, password2):
#         """
#         This function is used to simulate a register event for a new user on our register page.
#         We fill all the fields and check that the new user is allowed to register
#         :param username: string
#         :param name: string
#         :param surname: string
#         :param email: string
#         :param password: string
#         :return: void
#         """
#         return self.app.post('/register', data=dict(
#             username=username,
#             name=name,
#             surname=surname,
#             email=email1,
#             email2=email2,
#             password=password1,
#             password2=password2
#         ), follow_redirects=True)
#
#     def test_user_registration(self):
#         """
#         This method allows us to check that the registration of the users takes place without problems
#         We check that when a user registers, a successful message is flashed
#
#         We also check that in the following cases the user is not created (errors message are flashed
#         in the register page):
#         - Username already taken
#         - Email already taken
#         - Email not in the good format (not in xxx@xxx.xx)
#         - The two fields email aren't matching
#         - The two password fields aren't matching
#         :return: void
#         """
#         # We check that a user can register if all the correct info is typed in
#         # To check if the registration took place correctly, we check the logs
#         with self.assertLogs() as cm :
#             TestApplication.register(self, 'Username2',  'Name2', 'Surname2', 'test2@test.co', 'test2@test.co',
#                                           'password2', 'password2')
#         self.assertEqual(cm.records[0].msg, 'Successful registry')
#
#         #We check that a user can't register with the same username than an already existing user
#         rv2 = TestApplication.register(self, 'Username2',  'Name3', 'Surname3', 'test3@test.co', 'test3@test.co',
#                                        'password3', 'password3')
#         assert b'This username is already used, please use a different username.' in rv2.data
#
#         # We check that a user can't register with the same email than an already existing user
#         rv3 = TestApplication.register(self, 'Username3', 'Name3', 'Surname3', 'test2@test.co', 'test2@test.co',
#                                        'password3', 'password3')
#         assert b'This e-mail is already used, please use a different email address.' in rv3.data
#
#         # We check that the user must type in an email that matches the email format
#         rv4 = TestApplication.register(self, 'Username3', 'Name3', 'Surname3', 'test3test.co', 'test3test.co',
#                                        'password3', 'password3')
#         assert b'Invalid email address.' in rv4.data
#
#         # We check that a user can't register if the validation email isn't equal to the email first typed in
#         rv5 = TestApplication.register(self, 'Username3', 'Name3', 'Surname3', 'test3@test.co', 'test3@test.com',
#                                        'password3', 'password3')
#         assert b'Field must be equal to email.' in rv5.data
#
#         # We check that a user can't register if the validation password isn't equal to the password first typed in
#         rv6 = TestApplication.register(self, 'Username3', 'Name3', 'Surname3', 'test3@test.co', 'test3@test.co',
#                                        'password3', 'password3x')
#         assert b'Field must be equal to password.' in rv6.data
#
#
#     def login(self, username, password):
#         """
#         This function is used to simulate a login event for a user on our login page.
#         We fill all the fields and check that the user is allowed to login
#         :param username: string
#         :param password: string
#         :return: void
#         """
#         return self.app.post('/login', data=dict(
#             username=username,
#             password=password
#         ), follow_redirects=True)
#
#     def logout(self):
#         """
#         Method allowing us to logout a user
#         :return: void
#         """
#         return self.app.get('/logout', follow_redirects=True)

    # def test_user_login_logout(self):
    #     """
    #     This method allows us to check that the login of the users takes place without problems
    #     We check that when a user logs in, a successful message is flashed
    #
    #     We also check that a user can't login if he types in the wrong info (wrong username or wrong password)
    #     :return: void
    #     """
    #     # We check that a user can log in if all the correct info is typed in
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                                  'password', 'password')
    #     with self.assertLogs() as cm:
    #         TestApplication.login(self, 'Username',  'password')
    #     self.assertEqual(cm.records[1].msg, 'Successful Login !')
    #
    #     # We check that the logout is succesful
    #     with self.assertLogs() as cm:
    #         self.logout()
    #     self.assertEqual(cm.records[0].msg, 'Successful Logout !')
    #
    #     # We check that a user can't log in if there is a mistake in its username
    #     with self.assertLogs() as cm:
    #         TestApplication.login(self, 'Username2', 'password')
    #     self.assertEqual(cm.records[1].msg, 'Invalid Username !')
    #
    #     # We check that a user can't log in if there is a mistake in its password
    #     with self.assertLogs() as cm:
    #         TestApplication.login(self, 'Username', 'password2')
    #     self.assertEqual(cm.records[1].msg, 'Invalid Password !')
    #
    # def test_routes_serie(self):
    #     """
    #     This method allows us to check the route for the serie template
    #     We check that a logged in user can access a serie if the id of the serie matches a serie in the api
    #     We also check that if the id is not correct, the user is correctly sent to an error template
    #     Finally, we check that a user can't go to a serie page if he isn't logged in
    #     :return: void
    #     """
    #     # We create a user that logs in that will be used throughout this test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # We check that the serie route works well with a correct id of a serie (1412 serie : Arrow)
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Successful query for the Serie id=1412 page')
    #
    #     # We check that an error is returned when an incorrect serie number is given
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/141213243', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Incorrect Serie id')
    #
    #     #We now check that this route is not available if no user is logged in
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_routes_movie(self):
    #     """
    #         This method allows us to check the route for the movie template
    #         We check that a logged in user can access a movie if the id of the movie matches a movie in the api
    #         We also check that if the id is not correct, the user is correctly sent to an error template
    #         Finally, we check that a user can't go to a movie page if he isn't logged in
    #         :return: void
    #     """
    #     # We create a user that logs in that will be used throughout this test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # We check that the movie route works well with the 475557 movie (Joker)
    #     with self.assertLogs() as cm:
    #         self.app.get('/movie/475557', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Successful query for the Movie id=475557 page')
    #
    #     # We check that an error is returned when an incorrect movie number is given
    #     with self.assertLogs() as cm:
    #         self.app.get('/movie/141213243', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Incorrect Movie id')
    #
    #     #We now check that this route is not available if no user is logged in
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/movie/1412', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_addSerie(self):
    #     """
    #     Cette methode nous permet de tester la route pour ajouter une serie a un utilisateur dans la base de donnees
    #     On verifie que quand l'utilisateur ajoute une serie, la bonne serie est ajoutee dans la table UserMedia
    #     On verifie egalement qu'il n'y a pas de soucis lors de l'ajout d'une deuxieme serie
    #     Puis, on verifie que lorsque l'utilisateur ajoute une serie deja presente dans ses series, rien ne se passe
    #     Enfin, on verifie que le login est demande avant d'ajouter une serie
    #     :return: void
    #     """
    #     # On crée un utilisateur utilise dans ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On verifie que la route serie marche bien
    #     with self.assertLogs() as cm:
    #         self.app.get('/add_serie/1412', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Serie 1412 successfully added')
    #
    #     # On verifie que la bonne serie est ajoutee et que l'episode en cours est bien S1E1
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
    #     self.assertEqual(len(serie), 1)
    #     self.assertEqual(serie[0].season_id, 1)
    #     self.assertEqual(serie[0].episode_id, 1)
    #
    #     # On verifie que l'ajout d'une deuxieme serie ne pose pas de probleme
    #     self.app.get('/add_serie/2190', follow_redirects=True)
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.all()
    #     self.assertEqual(len(serie), 2)
    #
    #     # On verifie que lorsqu'on ajoute une serie deja presente, rien ne se passe
    #     self.app.get('/add_serie/1412', follow_redirects=True)
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
    #     self.assertEqual(len(serie), 1)
    #
    #     # Finalement, on verifie que si l'utilisateur n'est pas connecté, il ne peut ajouter une serie
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/add_serie/2190', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_removeSerie(self):
    #     """
    #     Cette methode nous permet de tester la route qui retire une serie d'un utilisateur dans la base de donnes
    #     On verifie que lorsque l'utilisateur retire une serie, la correcte serie est retiree de la base de donnes
    #     On verifie que si l'utilisateur retire une serie qu'il n'a deja pas, rien ne se passe
    #     On verifie egalement qu'il y a besoin que l'utilisateur soit login
    #     :return: void
    #     """
    #     # On cree l'utilisateur utilise dans ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On ajoute 1 serie a l'utilisateur
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_serie(1412)
    #
    #     # On verifie que la route fonctionne bien
    #     with self.assertLogs() as cm:
    #         self.app.get('/remove_serie/1412', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Serie 1412 successfully removed')
    #     # On verifie que la serie est bien retiree de la base de donnes
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
    #     self.assertEqual(serie, [])
    #
    #     # On ajoute 1 serie a l'utilisateur
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_serie(1412)
    #     self.app.get('/remove_serie/1413', follow_redirects=True)
    #     # On verifie que rien n'a change dans la base de donnes
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
    #     self.assertEqual(len(serie), 1)
    #
    #     # On verifie que la route n'est pas atteignable lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/remove_serie/2190', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_addMovie(self):
    #     """
    #     Cette methode nous permet de tester la route pour l'ajout d'un film dans la base de donnes
    #     On verifie que lorsque cette route est utilisee, le film est ajoute a la route
    #     On verifie que lorsque le film est deja dans la base de donnees, rien ne se passe
    #     On verifie egalement que le login est necessaire
    #     :return: void
    #     """
    #     # On cree un utilisateur qui nous servira pendant ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On verifie que la route fonctionne bien
    #     with self.assertLogs() as cm:
    #         self.app.get('/add_movie/475557', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Movie 475557 successfully added')
    #     # On verifie que le film est bien ajoute dans la base de donnes
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.all()
    #     self.assertEqual(serie[0].media_id, 475557)
    #
    #     # On verifie qu'on ne peut ajouter 2 fois le meme film dans la base de donnes
    #     self.app.get('/add_movie/475557', follow_redirects=True)
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='movie', media_id=475557).all()
    #     self.assertEqual(len(serie), 1)
    #
    #     # On verifie que la route n'est pas utilisable lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/add_movie/420818', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_removeMovie(self):
    #     """
    #     Cette methode nous permet de tester la route en charge de retirer un film aux filmsde l'utilisateur
    #     On verifie que lorsqu'un utilisateur retire un film, le bon est retire de la base de donnes
    #     On verifie egalement que lorsque l'utilisateur retire un film non dans la base de donnes, rien ne se passe
    #     Enfin, on verifie qu'il faut etre connecte pour retirer un film
    #     :return: void
    #     """
    #     # On cree un utilisateur utilise pendant tout le test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On lui ajoute 2 films :
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_movie('475557')
    #     u[0].add_movie(420818)
    #
    #     # On verifie que la route fonctionne bien
    #     with self.assertLogs() as cm:
    #         self.app.get('/remove_movie/475557', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Movie 475557 successfully removed')
    #     # On verifie que le film est bien retire de la base de donnees
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='movie', media_id=475557).all()
    #     self.assertEqual(serie, [])
    #
    #     # On verifie maintenant que si l'on supprime un film qui n'est pas dans la base de donnees, rien ne se passe
    #     self.app.get('/remove_movie/475557', follow_redirects=True)
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='movie').all()
    #     self.assertEqual(len(serie), 1)
    #
    #     # On verifie desormais que la route ne marche pas si l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/remove_movie/420818', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_mySerie(self):
    #     """
    #     Avec cette methode, on teste la route mySerie
    #     On verifie que les series sont affichees lorsque l'utiliseur en a et que rien n'est affiche s'il n'en a pas
    #     Enfin, on verifie que lorsque l'utilisateur est deconnecte, la page ne peut pas etre affiche
    #     :return: void
    #     """
    #     # On cree un utilisateur utilise pendant tout le test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On ajoute 2 series a l'utilisateur
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_serie(1412)
    #     u[0].add_serie(2190)
    #
    #     # On verifie que la route fonctionne correctement
    #     with self.assertLogs() as cm:
    #         self.app.get('/myseries', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'MySeries page rendered')
    #     self.assertEqual(cm.records[1].msg, 'The series list has 2 series')
    #
    #     # On verifie que lorsque l'utilisateur n'a aucune serie, la route indique que la page n'a pas de serie
    #     u = User.query.filter_by(name='Name')
    #     u[0].remove_serie(1412)
    #     u[0].remove_serie(2190)
    #     with self.assertLogs() as cm:
    #         self.app.get('/myseries', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'MySeries page rendered without series')
    #
    #     # On verifie que la route n'est pas atteignable si l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/myseries', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_myMovie(self):
    #     """
    #     Cette methode nous permet de verifier que la route myMovies fonctionne bien
    #     On verifie que les films sont affiches lorsque l'utiliseur en a et que rien n'est affiche s'il n'en a pas
    #     Enfin, on verifie que lorsque l'utilisateur est deconnecte, la route ne fonctionne pas
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On lui ajoute 2 films
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_movie(453405)
    #     u[0].add_movie('420818')
    #
    #     # On verifie que la route fonctionne bien
    #     with self.assertLogs() as cm:
    #         self.app.get('/mymovies', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'MyMovies page rendered')
    #     self.assertEqual(cm.records[1].msg, 'The movies list has 2 movies')
    #
    #     # On verifie que quand l'utilisateur n'a pas de film, la route indique que l'utilisateur n'a pas de films
    #     u = User.query.filter_by(name='Name')
    #     u[0].remove_movie(453405)
    #     u[0].remove_movie('420818')
    #     with self.assertLogs() as cm:
    #         self.app.get('/mymovies', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'MyMovies page rendered without movies')
    #
    #     # Enfin, on verifie que l'utilisateur doit etre connecte pour suivre cette route
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/mymovies', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_search(self):
    #     """
    #     On verifie que la route pour search2 retourne la bonne recherche pour l'utilisateur
    #     On verifie egalement que la route ne fonctionne pas si l'utilisateur n'est pas connecte
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On verifie que la recherche est bien celle attendue
    #     with self.assertLogs() as cm:
    #         self.app.get('/search2/test/1', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Search page 1 rendered for : test')
    #
    #     # On verifie que la route n'est pas utilisable lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/search2/test/1', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_genre(self):
    #     """
    #     On verifie avec cette methode la route genre
    #     On verifie donc que la route renvoie le bon genre pour l'utilisateur
    #     On verifie egalement que l'utilisateur ne peut acceder a cette route s'il n'est pas connecte
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On verifie que la route renvoie le bon genre
    #     with self.assertLogs() as cm:
    #         self.app.get('/genre/tv/Comedy/1', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Genre request on : Genre = Comedy, Media = serie, Page = 1')
    #
    #     # On verifie que le genre n'est pas atteignable si l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/genre/tv/Comedy/1', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_select_episode(self):
    #     """
    #     On verifie avec cette methode que la route pour selectionner un episode renvoie le bon episode
    #     On verifie egalement que l'utilisateur ne peut pas regarder un episode lorsque non connecte
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On verifie que la route redirige vers le bon episode de la serie
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412/season/3/episode/4', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Selected Episode : Serie = 1412, Season = 3, episode = 4')
    #
    #     # On verifie egalement que si l'utilisateur n'est pas connecte, on ne peut afficher les episodes
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412/season/3/episode/4', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_route_upcomingEpisodes(self):
    #     """
    #     On verifie que les series sont ajoutees dans les bonnes listes pour l'utilisateur
    #     On doit verifier que :
    #     - Les series en cours a jour sont ajoutees dans les series up_to_date
    #     - Les series finies sont ajoutees aux series finished
    #     - Les series non a jour sont ajoutees aux series not_up_to_date
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On ajoute 3 series pour l'utilisateur : Arrow(1412) qui ne sera pas une serie a jour, Friends (1668) qui sera
    #     # un show termine (on va mettre comme episode vu par l'utilisateur, le dernier episode) et Flash(60735) sera
    #     # la serie en cours : on va ajouter le dernier episode (en cours en ce moment)
    #     u = User.query.filter_by(name='Name')
    #     # on recupere les infos de la serie Flash
    #     serie = Api.get_serie(60735)
    #     latest_season, latest_ep = serie.latest['season_number'], serie.latest['episode_number']
    #     u[0].add_serie(1412)
    #     u[0].add_serie(1668)
    #     # pour mettre à jour au bon episode
    #     u[0].view_episode(18, 10, 1668)
    #     u[0].add_serie(60735)
    #     u[0].view_episode(latest_ep, latest_season, 60735)
    #
    #     # On verifie que la route fonctionne bien
    #     with self.assertLogs() as cm:
    #         self.app.get('/upcoming', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Serie 60735 added to up to date shows')
    #     self.assertEqual(cm.records[1].msg, 'Serie 1412 added to not up to date shows')
    #     self.assertEqual(cm.records[2].msg, 'Serie 1668 added to finished shows')
    #
    #
    #     # On verifie egalement que si l'utilisateur n'est pas connecte, la route ne fonctionne pas
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/upcoming', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_next_episode(self):
    #     """
    #     Cette methode teste la route next_episode en s'assurant qu'elle marque l'episode vu
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On lui ajoute une serie
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_serie(1412)
    #
    #     # On verifie que l'episode est marque comme vu
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412/season/3/episode/4/view', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, f'The user marked S3E4 from serie 1412 as viewed')
    #
    #     # On verifie que la base de donnees s'est mise a jour
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
    #     self.assertEqual(serie[0].season_id, 3)
    #     self.assertEqual(serie[0].episode_id, 4)
    #
    #     # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412/season/3/episode/4/view', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_rate(self):
    #     """
    #     Cette methode permet de tester la route test_rate
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On verifie que la route fonctionne
    #     with self.assertLogs() as cm:
    #         self.app.get('/rate/2', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, f'The user is selecting the grade 4.0')
    #
    #     # On verifie que le champ current grade dans la base de donnees est mis a jour
    #     u = User.query.filter_by(name='Name')
    #     self.assertEqual(u[0].current_grade, 4.)
    #
    #     # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/rate/2', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_post_serie_grade(self):
    #     """
    #     Cette methode permet de tester la route post_serie_grade
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On lui ajoute une serie
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_serie(1412)
    #     u[0].update_grade(4)
    #
    #     # On verifie que la route fonctionne
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412/post/grade', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, f'The user posted the grade 4 for the serie 1412')
    #
    #     # On verifie que la note a ete ajoutee dans la base de donnes
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
    #     self.assertEqual(serie[0].media_grade, 4)
    #
    #     # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412/post/grade', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_post_movie_grade(self):
    #     """
    #     Cette methode permet de tester la route post_movie_grade
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On lui ajoute un film
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_movie(475557)
    #     u[0].update_grade(4)
    #
    #     # On verifie que la route fonctionne
    #     with self.assertLogs() as cm:
    #         self.app.get('/movie/475557/post/grade', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, f'The user posted the grade 4 for the movie 475557')
    #
    #     # On verifie que la note a ete ajoutee dans la base de donnes
    #     u = User.query.filter_by(name='Name')
    #     movie = u[0].user_media.filter_by(media='movie', media_id=475557).all()
    #     self.assertEqual(movie[0].media_grade, 4)
    #
    #     # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/movie/475557/post/grade', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_unrate_serie(self):
    #     """
    #     Cette methode permet de tester la route unrate_serie
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On lui ajoute une serie
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_serie(1412)
    #     u[0].grade(1412, 'serie', 4)
    #
    #     # On verifie que la route fonctionne
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412/unrate', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user unrated the serie 1412')
    #
    #     # On verifie que la note a ete retiree de la base de donnes
    #     u = User.query.filter_by(name='Name')
    #     serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
    #     self.assertIsNone(serie[0].media_grade)
    #
    #     # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/serie/1412/unrate', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_unrate_movie(self):
    #     """
    #     Cette methode permet de tester la route unrate_movie
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On lui ajoute une serie
    #     u = User.query.filter_by(name='Name')
    #     u[0].add_movie(475557)
    #     u[0].grade(475557, 'movie', 4)
    #
    #     # On verifie que la route fonctionne
    #     with self.assertLogs() as cm:
    #         self.app.get('/movie/475557/unrate', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user unrated the movie 475557')
    #
    #     # On verifie que la note a ete retiree de la base de donnes
    #     u = User.query.filter_by(name='Name')
    #     movie = u[0].user_media.filter_by(media='movie', media_id=475557).all()
    #     self.assertIsNone(movie[0].media_grade)
    #
    #     # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/movie/475557/unrate', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def test_topRated(self):
    #     """
    #     Cette methode teste la route topRated
    #     On verifie que lorsque cette methode est appelee, les bonnes pages sont affichees
    #     :return: void
    #     """
    #     # On cree un utilisateur pour ce test
    #     TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
    #                              'password', 'password')
    #     TestApplication.login(self, 'Username', 'password')
    #
    #     # On verifie que la route fonctionne
    #     with self.assertLogs() as cm:
    #         self.app.get('/topRated/tv/1', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Top Rated request on Media = tv, Page = 1')
    #
    #     with self.assertLogs() as cm:
    #         self.app.get('/topRated/movie/2', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'Top Rated request on Media = movie, Page = 2')
    #
    #     # On verifie que la route ne fonctionne pas si l'utilisateur n'est pas connecte
    #     self.logout()
    #     with self.assertLogs() as cm:
    #         self.app.get('/topRated/movie/1', follow_redirects=True)
    #     self.assertEqual(cm.records[0].msg, 'The user is logging in')
    #
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()


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

#
# class TestUser(TestCase):
#     user = User(username='Username', email='test@test.co', name='Name', surname='Surname')
#     user.set_password('password')
#
#     def test_check_password(self):
#         """
#         We check that the check_password method returns the correct results
#         (True if the correct password is given in input, False if not)
#         :return: void
#         """
#         assert self.user.check_password('password')
#         assert not self.user.check_password('password2')
#
#     def test_list_serie(self):
#         """
#         We check that this function returns the correct list of series of the user
#         We also check that if the user doesn't have any series, the correct result is returned
#         :return: void
#         """
#         # Our user doesn't have any series yet
#         assert self.user.list_serie() == "The user doesn't have any series"
#
#         # We now add 2 series to our user
#         self.user.series = '1412xS1E1-69050xS1E1'
#         assert self.user.list_serie() == ['1412', '69050']
#
#     def test_list_movie(self):
#         """
#         We check that this function returns the correct list of movies of the user
#         We also check that if the user doesn't have any movies, the correct result is returned
#         :return: void
#         """
#         # Our user doesn't have any movies yet
#         self.assertEqual(self.user.list_movie(), "The user doesn't have any movie")
#
#         # We now add 2 movies to our user
#         self.user.movies = '453405-420818'
#         assert self.user.list_movie() == ['453405', '420818']
#
#     def test_is_in_series(self):
#         """
#         We check that the is_in_series method returns the correct answer :
#             - True if the serie is in the serie list of the user
#             - False if the serie isn't in the serie list of the user
#         :return: void
#         """
#         # We check that the answer is True when the serie is in the user list
#         self.user.series = '1412xS1E1-69050xS1E1'
#         self.assertTrue(self.user.is_in_series('1412'))
#
#         # We check that the answer is False when the serie isn't in the  user list
#         self.assertFalse(self.user.is_in_series('1413'))
#
#         # We check that when the user serie list is none no answer is raised
#         TestUser.user.series = None
#         self.assertFalse(self.user.is_in_series('1412'))
#         self.user.series = ''
#         self.assertFalse(self.user.is_in_series('1412'))
#
#     def test_has_movie(self):
#         """
#         We check that the has_movie method returns the correct answer :
#             - True if the movie in sin the movie list of the user
#             - False if the movie isn't in the movie list of the user
#         :return: void
#         """
#         # We check that the answer is True when the serie is in the user list
#         self.user.movies = '453405-420818'
#         self.assertTrue(self.user.has_movie('453405'))
#
#         # We check that the answer is False when the movie isn't in the user list
#         self.assertFalse(self.user.has_movie('453403'))
#
#         # We check that when the user movie list is none no answer is raised
#         TestUser.user.movies = None
#         self.assertFalse(self.user.has_movie('1412'))
#         self.user.movies = ''
#         self.assertFalse(self.user.has_movie('1412'))
#
#     def test_get_last_episode_viewed(self):
#         """
#         We check that the get_last_episode_viewed method returns the correct answer :
#             - None if the serie isn't in the series list of the user
#             - The last episode if the serie is in the list
#         :return: void
#         """
#         # We check that the answer is the correct episode when the serie is in the user list
#         self.user.series = '1412xS3E4-69050xS1E1'
#         self.assertEqual(self.user.get_last_episode_viewed('1412'), 'S3E4')
#
#         # We check that the answer is None
#         self.assertIsNone(self.user.get_last_episode_viewed('1413'))
#
#     def test_is_after(self):
#         """
#         We check that the is_after method returns the correct answer :
#             - True if the episode is after the last episode viewed by the user
#             - Returns true if the serie isn't in the serie list of the user
#         :return: void
#         """
#         # We check that the method returns true if we take an episode from the same season as the last episode
#         # viewed but with an higher number
#         self.user.series = '1412xS3E4-69050xS1E1'
#         self.assertTrue(self.user.is_after(3, 5, 1412))
#
#         # We also check that it returns true if the episode is from a next season
#         self.assertTrue(self.user.is_after(4, 2, 1412))
#
#         # We check that it returns true if the serie isn't in the serie list
#         self.assertTrue(self.user.is_after(1, 1, 1413))
#
#         # We check that it returns False if the episode is of the same season but earlier
#         self.assertFalse(self.user.is_after(3, 3, 1412))
#
#         # Finally, we check that it returns True if the episode is from an earlier season
#         self.assertFalse(self.user.is_after(1, 6, 1412))
#
#     def test_view_episode(self):
#         """
#         We check that the view_episode correctly updates the serie list to change the last viewed episode :
#         :return: void
#         """
#         # We check that the method updates the last episode the user saw
#         self.user.series = '1412xS3E4-69050xS1E1'
#         self.user.view_episode('S4E5', 1412)
#         self.assertEqual(self.user.get_last_episode_viewed(1412), 'S4E5')
#
#         # We check that no error is raised when we update a serie that isn't in the user list
#         self.user.view_episode('S5E6', 1413)
#         self.assertEqual(self.user.series, '1412xS4E5-69050xS1E1')
#
#     def test_add_serie(self):
#         """
#         We check that the add_serie method correctly adds the serie to the serie list of the user
#         If the user already has this serie in his list then it musn't add it again
#         We also need to check when the user has no serie in his list yet as the expected return is different
#             (no - in front in the list)
#         :return: void
#         """
#         # We set the serie list of our user to None and try to add a serie.
#         # We check that the output is the expecterd one
#         self.user.series = None
#         self.user.add_serie('1412')
#         self.assertEqual(self.user.series, '1412xS1E1')
#
#         # We now add another serie to the user serie list to check that we get the expected result (with a - in front)
#         self.user.add_serie('69050')
#         self.assertEqual(self.user.series, '1412xS1E1-69050xS1E1')
#
#         #Finally we check that when adding a serie already in the list, the method does nothing
#         self.user.add_serie('1412')
#         self.assertEqual(self.user.series, '1412xS1E1-69050xS1E1')
#
#     def test_remove_serie(self):
#         """
#         We check that the remove_serie method correctly removes the serie from the serie list of the user
#         If the user doesn't have this serie in its serie list then it musn't create an error
#         We also need to check when the user only has one serie in its list because the returned value is different
#             (no - in front in the list)
#         :return:
#         """
#         # We check that the method doesn't fail when we delete a serie that's not yet in the user's list
#         self.user.series = '1412xS3E4-69050xS1E1'
#         self.user.remove_serie('1413')
#         self.assertEqual(self.user.series, '1412xS3E4-69050xS1E1')
#
#         # We check that the method gives us the expected result when we delete a serie in the front of the list
#         self.user.remove_serie('1412')
#         self.assertEqual(self.user.series, '69050xS1E1')
#
#         # We check that the method gives us the expected result when we delete a serie in the back of the list
#         self.user.add_serie('1412')
#         self.user.remove_serie('1412')
#         self.assertEqual(self.user.series, '69050xS1E1')
#
#         # Finally we check that when deleting all the series from the list, no error is raised
#         self.user.remove_serie('69050')
#         self.assertEqual(self.user.series, '')
#
#     def test_add_movie(self):
#         """
#         We check that the add_movie method correctly adds the movie to the movie list of the user
#         If the user already has this movie in his list then it musn't add it again
#         We also need to check when the user has no movie in his list yet as the expected return is different
#             (no - in front in the list)
#         :return: void
#         """
#
#         # We set the movie list of our user to None and try to add a movie.
#         # We check that the output is the expecterd one
#         self.user.movies = None
#         self.user.add_movie('453405')
#         self.assertEqual(self.user.movies, '453405')
#
#         # We now add another movie to the user movie list to check that we get the expected result (with a - in front)
#         self.user.add_movie('420818')
#         self.assertEqual(self.user.movies, '453405-420818')
#
#         # Finally we check that when adding a serie already in the list, the method does nothing
#         self.user.add_movie('420818')
#         self.assertEqual(self.user.movies, '453405-420818')
#
#     def test_remove_movie(self):
#         """
#         We check that the remove_movie method correctly removes the movie from the movie list of the user
#         If the user doesn't have this movie in its movie list then it musn't create an error
#         We also need to check when the user only has one movie in its list because the returned value is different
#             (no - in front in the list)
#         :return:
#         """
#         # We check that the method doesn't fail when we delete a movie that's not yet in the user's list
#         self.user.movies = '453405-420818'
#         self.user.remove_movie('4534053')
#         self.assertEqual(self.user.movies, '453405-420818')
#
#         # We check that the method gives us the expected result when we delete a movie in the front of the list
#         self.user.remove_movie('453405')
#         self.assertEqual(self.user.movies, '420818')
#
#         # We check that the method gives us the expected result when we delete a movie in the back of the list
#         self.user.add_movie('453405')
#         self.user.remove_movie('453405')
#         self.assertEqual(self.user.movies, '420818')
#
#         # Finally we check that when deleting all the movies from the list, no error is raised
#         self.user.remove_movie('420818')
#         self.assertEqual(self.user.movies, '')
#
#     def test_update_grade(self):
#         """
#         We try here to check that the update_grade method works well, we check it in two context
#         (none current_grade and current_grade already filled)
#         :return: void
#         """
#         self.user.series = '1412xS3E4-69050xS1E1'
#         self.user.current_grade = None
#
#         # We test the method when the current_grade is None
#         self.user.update_grade(4)
#         self.assertTrue(self.user.current_grade, '4')
#
#         # We test the method when the current_grade is already filled
#         self.user.update_grade(2)
#         self.assertTrue(self.user.current_grade, '2')
#
#     def test_grade(self):
#         """
#         We need to test here that the grading of the medias is correct
#         We need to check both cases (TV show and media)
#         In both cases, we need to check the grading when there already is a grading before and when there isn't :
#             the grading list isn't under the same form in both cases
#         :return:
#         """
#         self.user.series_grades = None
#         self.user.movies_grades = None
#
#         # We check that when adding a grade to a serie with an empty grade list there is no problem
#         self.user.grade('1412', 'serie', 2)
#         self.assertEqual(self.user.series_grades, '1412x2')
#
#         # We check that when adding a grade to a movie with an empty grade list there is no problem
#         self.user.grade('453405', 'movie', 4)
#         self.assertEqual(self.user.movies_grades, '453405x4')
#
#         # We check that the method works well when there already is a grade in the serie grade list
#         self.user.grade('69050', 'serie', 8)
#         self.assertEqual(self.user.series_grades, '1412x2-69050x8')
#
#         # We check that the method works well when there already is a grade in the movie grade list
#         self.user.grade('420818', 'movie', 6)
#         self.assertEqual(self.user.movies_grades, '453405x4-420818x6')
#
#     def test_is_graded(self):
#         """
#         We try here to check that the is_graded method works well, for both series and movies
#         We need to check that when the media is graded, the method returns True
#         The method needs to return False when the media is not graded or the graded list is null
#         We need to check that it works for both series and movies
#         :return: void
#         """
#         self.user.series_grades = None
#         self.user.movies_grades = None
#
#         # We check that it returns false for both series and movies when the lists are None
#         self.assertFalse(self.user.is_graded('serie', '1412'))
#         self.assertFalse(self.user.is_graded('movie', '453405'))
#
#         # We now add a serie and a movie to the user grades lists
#         self.user.grade('1412', 'serie', 2)
#         self.user.grade('453405', 'movie', 8)
#
#         # We now check that the method returns true for both of them when we check that they are graded
#         self.assertTrue(self.user.is_graded('serie', '1412'))
#         self.assertTrue(self.user.is_graded('movie', '453405'))
#
#         # Finally we check that the method returns false when we look for others medias or other series/films
#         self.assertFalse(self.user.is_graded('serie', '1413'))
#         self.assertFalse(self.user.is_graded('movie', '453406'))
#         with self.assertRaises(ValueError):
#             self.user.is_graded('other_media', '1412')
#
#     def test_get_grade(self):
#         """
#         We try here to check that the get_grade method works well, for both series and movies
#         We need to check that when the media is graded, the method returns the grade
#         The method needs to return False when the media is not graded or the graded list is null
#         We need to check that it works for both series and movies
#         :return: void
#         """
#         self.user.series_grades = None
#         self.user.movies_grades = None
#
#         # We check that it returns false for both series and movies when the lists are None
#         self.assertFalse(self.user.get_grade('serie', '1412'))
#         self.assertFalse(self.user.get_grade('movie', '453405'))
#
#         # we add grades to the series and movies grades lists
#         self.user.grade('1412', 'serie', 2)
#         self.user.grade('453405', 'movie', 8)
#
#         # We check that we get the grades of the medias
#         self.assertEqual(self.user.get_grade('serie', '1412'), 2)
#         self.assertEqual(self.user.get_grade('movie', '453405'), 8)
#
#         # Finally we check that the method returns false when we grade for others medias or other series/films
#         self.assertFalse(self.user.is_graded('serie', '1413'))
#         self.assertFalse(self.user.is_graded('movie', '453406'))
#         with self.assertRaises(ValueError):
#             self.user.is_graded('other_media', '1412')
#
#     def test_unrate(self):
#         """
#            We try here to check that the unrate method works well, for both series and movies
#            We need to check that when the media is graded, the method deletes the grade and the media from the list
#            We also need to check that there are no errors if the lists are None
#            Finally we need to check that the delete works well when we delete the first media,
#            or when there only is one media
#            :return: void
#         """
#         self.user.series_grades = '1412x2-69050x6-62286x8'
#         self.user.movies_grades = '453405x4-420818x8-420809x6'
#
#         # We check that it returns the correct list when we delete the first elements
#         self.user.unrate('serie', '1412')
#         self.user.unrate('movie', '453405')
#         self.assertEqual(self.user.series_grades, '69050x6-62286x8')
#         self.assertEqual(self.user.movies_grades, '420818x8-420809x6')
#
#         # We check that it returns the correct list when we delete the last elements
#         self.user.unrate('serie', '62286')
#         self.user.unrate('movie', '420809')
#         self.assertEqual(self.user.series_grades, '69050x6')
#         self.assertEqual(self.user.movies_grades, '420818x8')
#
#         # We check that nothing happens when we delete a media not in the lists
#         self.user.unrate('serie', '62286')
#         self.user.unrate('movie', '420809')
#         self.assertEqual(self.user.series_grades, '69050x6')
#         self.assertEqual(self.user.movies_grades, '420818x8')
#
#         # Finally, we check that nothing happens when the list is None or empty
#         self.user.series_grades = None
#         self.user.movies_grades = None
#         self.user.unrate('serie', '62286')
#         self.user.unrate('movie', '420809')
#         self.assertEqual(self.user.series_grades, None)


if __name__ == '__main__':
    unittest.main()



