import os
import unittest
from app.api import Api
from classes.Exception import SetterException
from config import basedir
from app import app, db
from app.models import User, UserMedia
from unittest import TestCase
from classes.media import Media
from classes.episode import Episode


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
        Cette methode nous permet de verifier que la connexion d'un utilisateur se deroule sans probleme
        On verifie que lorsqu'il se connecte, les bons messages sont affiches
        On verifie egalement qu'un utilisateur ne peut se connecter avec des informations erronnees
        On verifie que les notifications sont egales a 1
        :return: void
        """
        # We check that a user can log in if all the correct info is typed in
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                     'password', 'password')

        with self.assertLogs() as cm:
            TestApplication.login(self, 'Username',  'password')
        self.assertEqual(cm.records[1].msg, 'Successful Login !')
        user = User.query.filter_by(name='Name')[0]
        self.assertEqual(user.notifications, bytes(1))

        # We check that the logout is succesful
        with self.assertLogs() as cm:
            self.logout()
        self.assertEqual(cm.records[0].msg, 'Successful Logout !')

        # We check that a user can't log in if there is a mistake in its username
        with self.assertLogs() as cm:
            TestApplication.login(self, 'Username2', 'password')
        self.assertEqual(cm.records[1].msg, 'Invalid Username !')

        # We check that a user can't log in if there is a mistake in its password
        with self.assertLogs() as cm:
            TestApplication.login(self, 'Username', 'password2')
        self.assertEqual(cm.records[1].msg, 'Invalid Password !')

    def test_routes_serie(self):
        """
        This method allows us to check the route for the serie template
        We check that a logged in user can access a serie if the id of the serie matches a serie in the api
        We also check that if the id is not correct, the user is correctly sent to an error template
        Finally, we check that a user can't go to a serie page if he isn't logged in
        :return: void
        """
        # We create a user that logs in that will be used throughout this test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # We check that the serie route works well with a correct id of a serie (1412 serie : Arrow)
        with self.assertLogs() as cm:
            self.app.get('/serie/1412', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Successful query for the Serie id=1412 page')

        # We check that an error is returned when an incorrect serie number is given
        with self.assertLogs() as cm:
            self.app.get('/serie/141213243', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Incorrect Serie id')

        #We now check that this route is not available if no user is logged in
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/serie/1412', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_routes_movie(self):
        """
            This method allows us to check the route for the movie template
            We check that a logged in user can access a movie if the id of the movie matches a movie in the api
            We also check that if the id is not correct, the user is correctly sent to an error template
            Finally, we check that a user can't go to a movie page if he isn't logged in
            :return: void
        """
        # We create a user that logs in that will be used throughout this test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # We check that the movie route works well with the 475557 movie (Joker)
        with self.assertLogs() as cm:
            self.app.get('/movie/475557', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Successful query for the Movie id=475557 page')

        # We check that an error is returned when an incorrect movie number is given
        with self.assertLogs() as cm:
            self.app.get('/movie/141213243', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Incorrect Movie id')

        #We now check that this route is not available if no user is logged in
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/movie/1412', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_addSerie(self):
        """
        Cette methode nous permet de tester la route pour ajouter une serie a un utilisateur dans la base de donnees
        On verifie que quand l'utilisateur ajoute une serie, la bonne serie est ajoutee dans la table UserMedia
        On verifie egalement qu'il n'y a pas de soucis lors de l'ajout d'une deuxieme serie
        Puis, on verifie que lorsque l'utilisateur ajoute une serie deja presente dans ses series, rien ne se passe
        Enfin, on verifie que le login est demande avant d'ajouter une serie
        :return: void
        """
        # On crée un utilisateur utilise dans ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')
        user = User.query.filter_by(name='Name')[0]

        # On verifie que la route serie marche bien
        with self.assertLogs() as cm:
            self.app.get('/add_serie/1412', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Serie 1412 successfully added')
        self.assertEqual(user.notifications, bytes(1))

        # On verifie que la bonne serie est ajoutee et que l'episode en cours est bien S1E1
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
        self.assertEqual(len(serie), 1)
        self.assertEqual(serie[0].season_id, 1)
        self.assertEqual(serie[0].episode_id, 1)

        # On verifie que l'ajout d'une deuxieme serie ne pose pas de probleme
        self.app.get('/add_serie/2190', follow_redirects=True)
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.all()
        self.assertEqual(len(serie), 2)

        # On verifie que lorsqu'on ajoute une serie deja presente, rien ne se passe
        self.app.get('/add_serie/1412', follow_redirects=True)
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
        self.assertEqual(len(serie), 1)

        # Finalement, on verifie que si l'utilisateur n'est pas connecté, il ne peut ajouter une serie
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/add_serie/2190', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_removeSerie(self):
        """
        Cette methode nous permet de tester la route qui retire une serie d'un utilisateur dans la base de donnes
        On verifie que lorsque l'utilisateur retire une serie, la correcte serie est retiree de la base de donnes
        On verifie que si l'utilisateur retire une serie qu'il n'a deja pas, rien ne se passe
        On verifie egalement qu'il y a besoin que l'utilisateur soit login
        :return: void
        """
        # On cree l'utilisateur utilise dans ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On ajoute 1 serie a l'utilisateur
        u = User.query.filter_by(name='Name')
        u[0].add_serie(1412)

        # On verifie que la route fonctionne bien
        with self.assertLogs() as cm:
            self.app.get('/remove_serie/1412', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Serie 1412 successfully removed')
        # On verifie que la serie est bien retiree de la base de donnes
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
        self.assertEqual(serie, [])

        # On ajoute 1 serie a l'utilisateur
        u = User.query.filter_by(name='Name')
        u[0].add_serie(1412)
        self.app.get('/remove_serie/1413', follow_redirects=True)
        # On verifie que rien n'a change dans la base de donnes
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
        self.assertEqual(len(serie), 1)

        # On verifie que la route n'est pas atteignable lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/remove_serie/2190', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_addMovie(self):
        """
        Cette methode nous permet de tester la route pour l'ajout d'un film dans la base de donnes
        On verifie que lorsque cette route est utilisee, le film est ajoute a la route
        On verifie que lorsque le film est deja dans la base de donnees, rien ne se passe
        On verifie egalement que le login est necessaire
        :return: void
        """
        # On cree un utilisateur qui nous servira pendant ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On verifie que la route fonctionne bien
        with self.assertLogs() as cm:
            self.app.get('/add_movie/475557', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Movie 475557 successfully added')
        # On verifie que le film est bien ajoute dans la base de donnes
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.all()
        self.assertEqual(serie[0].media_id, 475557)

        # On verifie qu'on ne peut ajouter 2 fois le meme film dans la base de donnes
        self.app.get('/add_movie/475557', follow_redirects=True)
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='movie', media_id=475557).all()
        self.assertEqual(len(serie), 1)

        # On verifie que la route n'est pas utilisable lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/add_movie/420818', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_removeMovie(self):
        """
        Cette methode nous permet de tester la route en charge de retirer un film aux filmsde l'utilisateur
        On verifie que lorsqu'un utilisateur retire un film, le bon est retire de la base de donnes
        On verifie egalement que lorsque l'utilisateur retire un film non dans la base de donnes, rien ne se passe
        Enfin, on verifie qu'il faut etre connecte pour retirer un film
        :return: void
        """
        # On cree un utilisateur utilise pendant tout le test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On lui ajoute 2 films :
        u = User.query.filter_by(name='Name')
        u[0].add_movie('475557')
        u[0].add_movie(420818)

        # On verifie que la route fonctionne bien
        with self.assertLogs() as cm:
            self.app.get('/remove_movie/475557', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Movie 475557 successfully removed')
        # On verifie que le film est bien retire de la base de donnees
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='movie', media_id=475557).all()
        self.assertEqual(serie, [])

        # On verifie maintenant que si l'on supprime un film qui n'est pas dans la base de donnees, rien ne se passe
        self.app.get('/remove_movie/475557', follow_redirects=True)
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='movie').all()
        self.assertEqual(len(serie), 1)

        # On verifie desormais que la route ne marche pas si l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/remove_movie/420818', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_mySerie(self):
        """
        Avec cette methode, on teste la route mySerie
        On verifie que les series sont affichees lorsque l'utiliseur en a et que rien n'est affiche s'il n'en a pas
        Enfin, on verifie que lorsque l'utilisateur est deconnecte, la page ne peut pas etre affiche
        :return: void
        """
        # On cree un utilisateur utilise pendant tout le test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On ajoute 2 series a l'utilisateur
        u = User.query.filter_by(name='Name')
        u[0].add_serie(1412)
        u[0].add_serie(2190)

        # On verifie que la route fonctionne correctement
        with self.assertLogs() as cm:
            self.app.get('/myseries', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'MySeries page rendered')
        self.assertEqual(cm.records[1].msg, 'The series list has 2 series')

        # On verifie que lorsque l'utilisateur n'a aucune serie, la route indique que la page n'a pas de serie
        u = User.query.filter_by(name='Name')
        u[0].remove_serie(1412)
        u[0].remove_serie(2190)
        with self.assertLogs() as cm:
            self.app.get('/myseries', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'MySeries page rendered without series')

        # On verifie que la route n'est pas atteignable si l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/myseries', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_myMovie(self):
        """
        Cette methode nous permet de verifier que la route myMovies fonctionne bien
        On verifie que les films sont affiches lorsque l'utiliseur en a et que rien n'est affiche s'il n'en a pas
        Enfin, on verifie que lorsque l'utilisateur est deconnecte, la route ne fonctionne pas
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On lui ajoute 2 films
        u = User.query.filter_by(name='Name')
        u[0].add_movie(453405)
        u[0].add_movie('420818')

        # On verifie que la route fonctionne bien
        with self.assertLogs() as cm:
            self.app.get('/mymovies', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'MyMovies page rendered')
        self.assertEqual(cm.records[1].msg, 'The movies list has 2 movies')

        # On verifie que quand l'utilisateur n'a pas de film, la route indique que l'utilisateur n'a pas de films
        u = User.query.filter_by(name='Name')
        u[0].remove_movie(453405)
        u[0].remove_movie('420818')
        with self.assertLogs() as cm:
            self.app.get('/mymovies', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'MyMovies page rendered without movies')

        # Enfin, on verifie que l'utilisateur doit etre connecte pour suivre cette route
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/mymovies', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_search(self):
        """
        On verifie que la route pour search2 retourne la bonne recherche pour l'utilisateur
        On verifie egalement que la route ne fonctionne pas si l'utilisateur n'est pas connecte
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On verifie que la recherche est bien celle attendue
        with self.assertLogs() as cm:
            self.app.get('/search2/test/1', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Search page 1 rendered for : test')

        # On verifie que la route n'est pas utilisable lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/search2/test/1', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_genre(self):
        """
        On verifie avec cette methode la route genre
        On verifie donc que la route renvoie le bon genre pour l'utilisateur
        On verifie egalement que l'utilisateur ne peut acceder a cette route s'il n'est pas connecte
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On verifie que la route renvoie le bon genre
        with self.assertLogs() as cm:
            self.app.get('/genre/tv/Comedy/1', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Genre request on : Genre = Comedy, Media = serie, Page = 1')

        # On verifie que le genre n'est pas atteignable si l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/genre/tv/Comedy/1', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_select_episode(self):
        """
        On verifie avec cette methode que la route pour selectionner un episode renvoie le bon episode
        On verifie egalement que l'utilisateur ne peut pas regarder un episode lorsque non connecte
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On verifie que la route redirige vers le bon episode de la serie
        with self.assertLogs() as cm:
            self.app.get('/serie/1412/season/3/episode/4', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Selected Episode : Serie = 1412, Season = 3, episode = 4')

        # On verifie egalement que si l'utilisateur n'est pas connecte, on ne peut afficher les episodes
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/serie/1412/season/3/episode/4', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_route_upcomingEpisodes(self):
        """
        On verifie que les series sont ajoutees dans les bonnes listes pour l'utilisateur
        On doit verifier que :
        - Les series en cours a jour sont ajoutees dans les series up_to_date
        - Les series finies sont ajoutees aux series finished
        - Les series non a jour sont ajoutees aux series not_up_to_date
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On ajoute 3 series pour l'utilisateur : Arrow(1412) qui ne sera pas une serie a jour, Friends (1668) qui sera
        # un show termine (on va mettre comme episode vu par l'utilisateur, le dernier episode) et Flash(60735) sera
        # la serie en cours : on va ajouter le dernier episode (en cours en ce moment)
        u = User.query.filter_by(name='Name')
        # on recupere les infos de la serie Flash
        serie = Api.get_serie(60735)
        latest_season, latest_ep = serie.latest['season_number'], serie.latest['episode_number']
        u[0].add_serie(1412)
        u[0].add_serie(1668)
        # pour mettre à jour au bon episode
        u[0].view_episode(18, 10, 1668)
        u[0].add_serie(60735)
        u[0].view_episode(latest_ep, latest_season, 60735)

        # On verifie que la route fonctionne bien
        with self.assertLogs() as cm:
            self.app.get('/upcoming', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Serie 60735 added to up to date shows')
        self.assertEqual(cm.records[1].msg, 'Serie 1412 added to not up to date shows')
        self.assertEqual(cm.records[2].msg, 'Serie 1668 added to finished shows')
        u = User.query.filter_by(name='Name')
        self.assertEqual(u[0].notifications, bytes(0))


        # On verifie egalement que si l'utilisateur n'est pas connecte, la route ne fonctionne pas
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/upcoming', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_next_episode(self):
        """
        Cette methode teste la route next_episode en s'assurant qu'elle marque l'episode vu
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On lui ajoute une serie
        u = User.query.filter_by(name='Name')
        u[0].add_serie(1412)

        # On verifie que l'episode est marque comme vu et que les notifications sont remises a 1
        with self.assertLogs() as cm:
            self.app.get('/serie/1412/season/3/episode/4/view', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, f'The user marked S3E4 from serie 1412 as viewed')
        self.assertEqual(u[0].notifications, bytes(1))

        # On verifie que la base de donnees s'est mise a jour
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
        self.assertEqual(serie[0].season_id, 3)
        self.assertEqual(serie[0].episode_id, 4)

        # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/serie/1412/season/3/episode/4/view', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_rate(self):
        """
        Cette methode permet de tester la route test_rate
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On verifie que la route fonctionne
        with self.assertLogs() as cm:
            self.app.get('/rate/2', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, f'The user is selecting the grade 4.0')

        # On verifie que le champ current grade dans la base de donnees est mis a jour
        u = User.query.filter_by(name='Name')
        self.assertEqual(u[0].current_grade, 4.)

        # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/rate/2', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_post_serie_grade(self):
        """
        Cette methode permet de tester la route post_serie_grade
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On lui ajoute une serie
        u = User.query.filter_by(name='Name')
        u[0].add_serie(1412)
        u[0].update_grade(4)

        # On verifie que la route fonctionne
        with self.assertLogs() as cm:
            self.app.get('/serie/1412/post/grade', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, f'The user posted the grade 4 for the serie 1412')

        # On verifie que la note a ete ajoutee dans la base de donnes
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
        self.assertEqual(serie[0].media_grade, 4)

        # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/serie/1412/post/grade', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_post_movie_grade(self):
        """
        Cette methode permet de tester la route post_movie_grade
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On lui ajoute un film
        u = User.query.filter_by(name='Name')
        u[0].add_movie(475557)
        u[0].update_grade(4)

        # On verifie que la route fonctionne
        with self.assertLogs() as cm:
            self.app.get('/movie/475557/post/grade', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, f'The user posted the grade 4 for the movie 475557')

        # On verifie que la note a ete ajoutee dans la base de donnes
        u = User.query.filter_by(name='Name')
        movie = u[0].user_media.filter_by(media='movie', media_id=475557).all()
        self.assertEqual(movie[0].media_grade, 4)

        # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/movie/475557/post/grade', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_unrate_serie(self):
        """
        Cette methode permet de tester la route unrate_serie
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On lui ajoute une serie
        u = User.query.filter_by(name='Name')
        u[0].add_serie(1412)
        u[0].grade(1412, 'serie', 4)

        # On verifie que la route fonctionne
        with self.assertLogs() as cm:
            self.app.get('/serie/1412/unrate', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user unrated the serie 1412')

        # On verifie que la note a ete retiree de la base de donnes
        u = User.query.filter_by(name='Name')
        serie = u[0].user_media.filter_by(media='serie', media_id=1412).all()
        self.assertIsNone(serie[0].media_grade)

        # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/serie/1412/unrate', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_unrate_movie(self):
        """
        Cette methode permet de tester la route unrate_movie
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On lui ajoute une serie
        u = User.query.filter_by(name='Name')
        u[0].add_movie(475557)
        u[0].grade(475557, 'movie', 4)

        # On verifie que la route fonctionne
        with self.assertLogs() as cm:
            self.app.get('/movie/475557/unrate', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user unrated the movie 475557')

        # On verifie que la note a ete retiree de la base de donnes
        u = User.query.filter_by(name='Name')
        movie = u[0].user_media.filter_by(media='movie', media_id=475557).all()
        self.assertIsNone(movie[0].media_grade)

        # On verifie que cette route ne peut etre suivie lorsque l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/movie/475557/unrate', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def test_topRated(self):
        """
        Cette methode teste la route topRated
        On verifie que lorsque cette methode est appelee, les bonnes pages sont affichees
        :return: void
        """
        # On cree un utilisateur pour ce test
        TestApplication.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')
        TestApplication.login(self, 'Username', 'password')

        # On verifie que la route fonctionne
        with self.assertLogs() as cm:
            self.app.get('/topRated/tv/1', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Top Rated request on Media = tv, Page = 1')

        with self.assertLogs() as cm:
            self.app.get('/topRated/movie/2', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'Top Rated request on Media = movie, Page = 2')

        # On verifie que la route ne fonctionne pas si l'utilisateur n'est pas connecte
        self.logout()
        with self.assertLogs() as cm:
            self.app.get('/topRated/movie/1', follow_redirects=True)
        self.assertEqual(cm.records[0].msg, 'The user is logging in')

    def tearDown(self):
        db.session.remove()
        db.drop_all()


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


class TestUser(TestCase):

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

    def test_check_password(self):
        """
        On verifie que la methode check_password retourne les bons resultats (vrai si le bon mot de passe est donne
        en entree, faux sinon)
        :return: void
        """
        # On cree un utilisateur utilise pendant tout le test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                                 'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        assert user.check_password('password')
        assert not user.check_password('password2')

    def test_list_serie(self):
        """
        On regarde si la methode list_serie retourne bien la liste des series de l'utilisateur
        On verifie que si l'utilisateur n'a aucune serie, le bon resultat est renvoye
        :return: void
        """
        # On cree un utilisateur utilise pendant tout le test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]
        user2 = User(name='Name2', username='Username2', email='test2@test.co')

        # Notre utilisateur n'a pas encore de series
        assert user.list_serie() == []

        # On lui ajoute deux series
        # Pour tester que la methode fait ce que l'on veut, on ajoute une serie a un autre utilisateur (user2)
        # On ajoute egalement un film a l'utilisateur user pour verifier que la methode fait ce que l'on veut
        s1 = UserMedia(media='serie', media_id=1412, season_id=1, episode_id=1, state_serie='nutd', user=user)
        s2 = UserMedia(media='serie', media_id=69050, season_id=1, episode_id=1, state_serie='nutd', user=user)
        s3 = UserMedia(media='serie', media_id=1668, season_id=1, episode_id=1, state_serie='nutd', user=user2)
        m1 = UserMedia(media='movie', media_id=453405, user=user)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        # On verifie que l'utilisateur a bien les series ajoutees
        self.assertEqual(user.list_serie(), [1412, 69050])

    def test_list_movie(self):
        """
        Avec cette methode, on teste la methode list_movie de la classe User
        On verifie que cette methode nous renvoie la bonne liste de series
        On verifie egalement que si l'utilisateur n'a aucune serie, il n'y a aucune serie renvoyee
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]
        user2 = User(name='Name2', username='Username2', email='test2@test.co')
        # Cet utilisateur n'a pas encore de series
        self.assertEqual(user.list_movie(), [])

        # On lui ajoute deux films a l'utilisateur 1
        # Pour tester que la methode fait ce que l'on veut, on ajoute un film  a un autre utilisateur (user2)
        # On ajoute egalement une serie a l'utilisateur 1 pour verifier que la methode fait ce que l'on veut
        m1 = UserMedia(media='movie', media_id=453405, user=user)
        m2 = UserMedia(media='movie', media_id=420818, user=user)
        m3 = UserMedia(media='movie', media_id=453405, user=user2)
        s2 = UserMedia(media='serie', media_id=1412, season_id=1, episode_id=1, state_serie='nutd', user=user)
        db.session.add(m1)
        db.session.add(m2)
        db.session.add(s2)
        db.session.add(m3)
        db.session.commit()
        self.assertEqual(user.list_movie(), [453405, 420818])

    def test_is_in_series(self):
        """
        On verifie que la methode is_in_series renvoie la bonne reponse :
         - True si la serie est dans la liste de l'utilisateur
         - Faux sinon
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]
        user2 = User(name='Name2', username='Username2', email='test2@test.co')

        # On ajoute 2 series a user
        # On lui ajoute egalement un film pour tester que la methode renvoie ce que l'on veut
        # On ajoute une serie a l'utilisateur user2 pour tester que la methode ne regarde que les series de user
        m1 = UserMedia(media='movie', media_id=453405, user=user)
        s1 = UserMedia(media='serie', media_id=1412, season_id=1, episode_id=1, state_serie='nutd', user=user)
        s2 = UserMedia(media='serie', media_id=69050, season_id=1, episode_id=1, state_serie='nutd', user=user)
        s3 = UserMedia(media='serie', media_id=1668, season_id=1, episode_id=1, state_serie='nutd', user=user2)
        db.session.add(m1)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()

        # On teste que la methode marche pour les series de l'utilisateur
        self.assertTrue(user.is_in_series(1412))

        # On teste que la methode ne regarde pas les films
        self.assertFalse(user.is_in_series(453405))

        # On teste que la methode ne regarde que les series de user
        self.assertFalse(user.is_in_series(1668))

    def test_has_movie(self):
        """
        On verifie que la methode has_movie retourne la bonne reponse :
        - True si le film est dans les films de l'utilisateur
        - False sinon
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]
        user2 = User(name='Name2', username='Username2', email='test2@test.co')

        # On ajoute 2 films a user
        # On lui ajoute egalement une serie pour tester que la methode renvoie ce que l'on veut
        # On ajoute un film a l'utilisateur user2 pour tester que la methode ne regarde que les films de user
        s1 = UserMedia(media='serie', media_id=1412, season_id=1, episode_id=1, state_serie='nutd', user=user)
        m1 = UserMedia(media='movie', media_id=420818, user=user)
        m2 = UserMedia(media='movie', media_id=453405, user=user)
        m3 = UserMedia(media='movie', media_id=501170, user=user2)
        db.session.add(s1)
        db.session.add(m1)
        db.session.add(m2)
        db.session.add(m3)
        db.session.commit()

        # On teste que la methode marche pour les films de l'utilisateur
        self.assertTrue(user.has_movie(420818))

        # On teste que la methode ne regarde pas les series
        self.assertFalse(user.has_movie(1412))

        # On teste que la methode ne regarde que les films de user
        self.assertFalse(user.is_in_series(501170))

    def test_get_last_episode_viewed(self):
        """
        On regarde que la methode get_last_episode_viewed retourne la bonne reponse :
            - S1E1 si la serie n'est pas dans la liste de l'utilisateur
            - Le dernier episode vu si la serie est dans la liste
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On verifie que si la serie est dans la liste de l'utilisateur, la methode renvoie bien le dernier episode
        s1 = UserMedia(media='serie', media_id=1412, season_id=3, episode_id=4, state_serie='nutd', user=user)
        db.session.add(s1)
        db.session.commit()
        self.assertEqual(user.get_last_episode_viewed('1412'), 'S3E4')

        # On verifie que si la serie n'est pas dans la liste de l'utilisateur, la methode renvoie S1E1
        self.assertEqual(user.get_last_episode_viewed('1413'), 'S1E1')

    def test_is_after(self):
        """
        Avec cette methode on va tester la methode is_after qui doit retourner :
            - True si l'episode en parametre est apres le dernier episode vu par l'utilisateur ou si la serie n'est
                    pas dans les series de l'utilisateur
            - False sinon
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On lui ajoute une serie
        s1 = UserMedia(media='serie', media_id=1412, season_id=3, episode_id=4, state_serie='nutd', user=user)
        db.session.add(s1)
        db.session.commit()

        # On verifie que la methode renvoie True si on lui donne en parametre un episode plus tard dans la meme saison
        self.assertTrue(user.is_after(season=3, episode=5, serie=1412))

        # On verifie que la methode renvoie True si on lui donne en parametre une saison plus tard que la saison du
        # dernier episode vu par l'utilisateur
        self.assertTrue(user.is_after(season=4, episode=2, serie=1412))

        # On verifie que la methode renvoie True si la serie n'est pas dans celles de l'utilisateur
        self.assertTrue(user.is_after(season=4, episode=2, serie=1413))

        # On verifie que la methode renvoie False dans les autres cas
        self.assertFalse(user.is_after(season=1, episode=10, serie=1412))
        self.assertFalse(user.is_after(season=3, episode=3, serie=1412))

    def test_view_episode(self):
        """
        Avec cette methode on va tester la methode view_episode qui doit effectue :
            Elle doit changer l'episode et la saison du dernier episode vu
            Elle doit changer le statut de la serie(utd/nutd/fin)
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On lui ajoute deux series (Friends serie qui n'est plus en production et Flash qui l'est encore)
        s1 = UserMedia(media='serie', media_id=1668, season_id=1, episode_id=1, state_serie='utd', user=user)
        s2 = UserMedia(media='serie', media_id=60735, season_id=1, episode_id=1, state_serie='fin', user=user)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        # On teste que la methode met a jour le dernier episode vu et le statut de ce dernier en nutd quand la
        # serie n'est pas a jour
        user.view_episode(season=3, episode=4, serie=1668)
        self.assertEqual(user.get_last_episode_viewed(id=1668), 'S3E4')
        status = user.user_media.filter_by(media='serie', media_id=1668).first().state_serie
        self.assertEqual(status, 'nutd')
        self.assertEqual(user.notifications, bytes(1))

        # On teste que la methode met a jour le dernier episode vu et le statut de ce dernier en fin quand la
        # serie est terminee (pas d'episode futur)
        user.view_episode(season=10, episode=18, serie=1668)
        self.assertEqual(user.get_last_episode_viewed(id=1668), 'S10E18')
        status = user.user_media.filter_by(media='serie', media_id=1668).first().state_serie
        self.assertEqual(status, 'fin')

        # On teste que la methode met a jour le dernier episode vu et le statut de ce dernier en fin quand la
        # serie est a jour (dernier episode vu mai il y a un episode futur) a l'aide de l'Api
        serie = Api.get_serie(60735)
        latest_season, latest_ep = serie.latest['season_number'], serie.latest['episode_number']
        user.view_episode(season=latest_season, episode=latest_ep, serie=60735)
        status = user.user_media.filter_by(media='serie', media_id=60735).first().state_serie
        self.assertEqual(status, 'utd')

    def test_add_serie(self):
        """
        Avec ce test on va tester la methode add_serie
        Celle-ci doit ajouter une serie donnee en parametre a l'utilisateur
        Si l'utilisateur a deja ajoute une serie, cette methode ne doit pas l'ajouter une deuxieme fois
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On ajoute une serie a notre utilisateur
        user.add_serie(1412)
        serie = user.user_media.filter_by(media='serie', media_id=1412).all()[0]
        self.assertEqual(serie.media_id, 1412)
        self.assertEqual(serie.season_id, 1)
        self.assertEqual(serie.episode_id, 1)
        self.assertEqual(serie.state_serie, 'nutd')

        # On lui rajoute une deuxieme serie et on verifie que la methode n'ajoute pas une deuxieme serie
        user.add_serie(1412)
        serie = user.user_media.filter_by(media='serie', media_id=1412).all()
        self.assertEqual(len(serie), 1)

    def test_remove_serie(self):
        """
        On regarde que la methode remove_serie retire correctement la serie des series de l'utilisateur
        Si l'utilisateur n'a pas cette serie dans ses series, la methode ne doit pas lever une erreur
        :return:
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On ajoute une serie a notre utilisateur
        user.add_serie(1412)
        user.add_movie(1413)

        # On verifie qu'il n'y a pas d'erreur lorsqu'on retire une serie qui n'est pas dans les series de l'utilisateur
        # On verifie egalement que la methode ne supprime pas un film ayant le meme id
        user.remove_serie(1413)
        media = user.user_media.all()
        self.assertEqual(len(media), 2)

        # On verifie que la methode retire bien une serie dans les series de l'utilisateur
        user.remove_serie(1412)
        serie = user.user_media.filter_by(media='serie', media_id=1412).all()
        self.assertEqual(serie, [])

    def test_add_movie(self):
        """
        Avec ce test on va tester la methode add_movie
        Celle-ci doit ajouter un film donnee en parametre a l'utilisateur
        Si l'utilisateur a deja ajoute un film, cette methode ne doit pas l'ajouter une deuxieme fois
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On ajoute un film a notre utilisateur
        user.add_movie(453405)
        movie = user.user_media.filter_by(media='movie', media_id=453405).all()[0]
        self.assertEqual(movie.media_id, 453405)

        # On lui rajoute une deuxieme le meme film et on verifie que la methode n'ajoute pas une deuxieme film
        user.add_movie(453405)
        movie = user.user_media.filter_by(media='movie', media_id=453405).all()
        self.assertEqual(len(movie), 1)

    def test_remove_movie(self):
        """
        On regarde que la methode remove_movie retire correctement le film des films de l'utilisateur
        Si l'utilisateur n'a pas ce film dans ses series, la methode ne doit pas lever une erreur
        :return:
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On ajoute un film a notre utilisateur
        user.add_movie(453405)
        user.add_serie(453406)

        # On verifie qu'il n'y a pas d'erreur lorsqu'on retire un film qui n'est pas dans les films de l'utilisateur
        # On verifie egalement que la methode ne supprime pas un film ayant le meme id
        user.remove_movie(453406)
        media = user.user_media.all()
        self.assertEqual(len(media), 2)

        # On verifie que la methode retire bien un film dans les films de l'utilisateur
        user.remove_movie(453405)
        movie = user.user_media.filter_by(media='movie', media_id=453405).all()
        self.assertEqual(movie, [])

    def test_update_grade(self):
        """
        On verifie ici que la methode update_grade fonctionne bien :
            Elle doit modifier la current_grade si cette dernière est vide ou pleine
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On lui ajoute une note
        user.update_grade(new_grade=4)
        self.assertEqual(user.current_grade, 4)

        # On modifie cette note
        user.update_grade(new_grade=6)
        self.assertEqual(user.current_grade, 6)

    def test_grade(self):
        """
        Ce test nous permet de tester la methode grade
        On va tester si cette methode marche pour les deux types de medias (tv et movie)
        Pour chaque cas, on va regarder le cas ou le media a deja une note, le cas ou il n'en a pas et le cas ou le
            media n'est pas dans les medias de l'utilisateur
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On lui ajoute une serie et un film
        user.add_movie(453405)
        user.add_serie(1412)

        # On note le film et la serie et on verifie que la notation marche bien
        user.grade(1412, 'serie', 4)
        user.grade(453405, 'movie', 6)
        serie = user.user_media.filter_by(media='serie', media_id=1412).first()
        movie = user.user_media.filter_by(media='movie', media_id=453405).first()
        self.assertEqual(serie.media_grade, 4)
        self.assertEqual(movie.media_grade, 6)

        # On change leurs notes et on verifie que la notation marche toujours bien
        user.grade(1412, 'serie', 5)
        user.grade(453405, 'movie', 7)
        serie = user.user_media.filter_by(media='serie', media_id=1412).first()
        movie = user.user_media.filter_by(media='movie', media_id=453405).first()
        self.assertEqual(serie.media_grade, 5)
        self.assertEqual(movie.media_grade, 7)

        # On va tenter de noter des medias qui ne sont pas dans les medias de l'utilisateur et
        # on va verifier que rien ne se passe
        # On change leurs notes et on verifie que la notation marche toujours bien
        user.grade(1413, 'serie', 6)
        user.grade(453406, 'movie', 8)
        serie = user.user_media.filter_by(media='serie').all()
        movie = user.user_media.filter_by(media='movie').all()
        self.assertEqual(len(serie), 1)
        self.assertEqual(len(movie), 1)
        self.assertEqual(serie[0].media_grade, 5)
        self.assertEqual(movie[0].media_grade, 7)

    def test_is_graded(self):
        """
        Ce test verifie que la methodeis_graded renvoie bien les valeurs attendues pour les series et les films
        On verifie que lorsqu'un media est note, la methode renvoie True
        La methode renvoie False sinon ou lorsque le media n'est pas dans les medias de l'utilisateur
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On lui ajoute une serie et un film
        user.add_movie(453405)
        user.add_serie(1412)

        # On verifie que la methode renvoie False si les deux medias ne sont pas notes
        self.assertFalse(user.is_graded('serie', 1412))
        self.assertFalse(user.is_graded('movie', 453405))

        # On verifie que la methode renvoie True si les deux medias sont notes
        user.grade(1412, 'serie', 4)
        user.grade(453405, 'movie', 6)
        self.assertTrue(user.is_graded('serie', 1412))
        self.assertTrue(user.is_graded('movie', 453405))

        # On verifie enfin que la methode renvoie false si les deux medias ne sont pas dans les medias de user
        self.assertFalse(user.is_graded('serie', 1413))
        self.assertFalse(user.is_graded('movie', 453406))

    def test_get_grade(self):
        """
        Ce test a pour objectif de tester la methode get_grade
        On va verifier qu'elle marche bien pour les series et les films
            - retourne la note si les medias sont notes
            - retourne False si les medias ne sont pas notes ou si les medias ne sont pas dans les medias de user
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On lui ajoute deux medias
        user.add_serie(1412)
        user.add_movie(420818)

        # On verifie que la methode renvoie False si les deux medias ne sont pas notes
        self.assertFalse(user.get_grade('serie', 1412))
        self.assertFalse(user.get_grade('movie', 420818))

        # On verifie que la methode renvoie True si les deux medias sont notes
        user.grade(1412, 'serie', 4)
        user.grade(420818, 'movie', 6)
        self.assertEqual(user.get_grade('serie', 1412), 4)
        self.assertEqual(user.get_grade('movie', 420818), 6)

        # On verifie enfin que la methode renvoie false si les deux medias ne sont pas dans les medias de user
        self.assertFalse(user.get_grade('serie', 1413))
        self.assertFalse(user.get_grade('movie', 420819))

    def test_unrate(self):
        """
        Dans cet test on va tester la methode unrate pour les series et les films
        On doit verifier que lorsqu'un media est note, la methode supprime la note de la table
        On verifie egalement qu'il n'y a pas d'erreurs si le media n'est pas note ou si le media n'est pas dans
            la liste
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On lui ajoute deux medias
        user.add_serie(1412)
        user.add_movie(420818)

        # On note les 2 medias
        user.grade(id=1412, type='serie', grade=4)
        user.grade(id=420818, type='serie', grade=8)

        # On verifie que la methode supprime bien les notes de ces medias
        user.unrate('serie', '1412')
        user.unrate('movie', '420818')
        serie = user.user_media.filter_by(media='serie', media_id=1412).all()[0]
        movie = user.user_media.filter_by(media='movie', media_id=420818).all()[0]
        self.assertIsNone(serie.media_grade)
        self.assertIsNone(movie.media_grade)

        # On verifie que la methode ne renvoie pas d'erreur lorsqu'on supprime et qu'il n'y a pas de notes
        user.unrate('serie', '1412')
        user.unrate('movie', '420818')
        serie = user.user_media.filter_by(media='serie', media_id=1412).all()[0]
        movie = user.user_media.filter_by(media='movie', media_id=420818).all()[0]
        self.assertIsNone(serie.media_grade)
        self.assertIsNone(movie.media_grade)

        # On verifie que la methode ne renvoie pas d'erreur lorsqu'on supprime des medias non dans les medias de user
        user.unrate('serie', '1413')
        user.unrate('movie', '420819')
        serie = user.user_media.filter_by(media='serie').all()
        movie = user.user_media.filter_by(media='movie').all()
        self.assertEqual(len(serie), 1)
        self.assertEqual(len(movie), 1)

    def test_update_all_upcoming_episodes(self):
        """
        Cet test verifie lamethodeupdate_all_upcoming_episodes:
        On verifie que tous les statuts de toutes les series sont mis à jour
        On va créer des series utd, nutd et fin pour verifier que tout est correctement mis ajour
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On lui ajoute trois series (Friends et How I Met your Mother, series qui n'est plus en production
        # et Flash qui l'est encore)
        # On ajoute egalement un film pour verifier qu'il n'y a pas d'erreur
        s1 = UserMedia(media='serie', media_id=1668, season_id=10, episode_id=18, state_serie='utd', user=user)
        s2 = UserMedia(media='serie', media_id=1100, season_id=5, episode_id=6, state_serie='fin', user=user)
        serie = Api.get_serie(60735)
        latest_season, latest_ep = serie.latest['season_number'], serie.latest['episode_number']
        s3 = UserMedia(media='serie', media_id=60735, season_id=latest_season, episode_id=latest_ep,
                       state_serie='nutd', user=user)
        user.add_movie(420818)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()

        # On teste que les statuts sont bien mis à jour
        user.update_all_upcoming_episodes()
        status1 = user.user_media.filter_by(media='serie', media_id=1668).first().state_serie
        status2 = user.user_media.filter_by(media='serie', media_id=1100).first().state_serie
        status3 = user.user_media.filter_by(media='serie', media_id=60735).first().state_serie
        self.assertEqual(status1, 'fin')
        self.assertEqual(status2, 'nutd')
        self.assertEqual(status3, 'utd')

    def test_check_upcoming_episodes(self):
        """
        Ce test verifie la methode upcoming_episodes
        On verifie que la valeur de retour est bien celle attendue
        :return:
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On verifie que la methode marche quand il n'y a pas de series
        self.assertEqual(user.check_upcoming_episodes(), ([], [], []))

        # On lui ajoute trois series (Friends et How I Met your Mother, series qui n'est plus en production
        # et Flash qui l'est encore)
        # On ajoute egalement un film pour verifier qu'il n'y a pas d'erreur
        s1 = UserMedia(media='serie', media_id=1668, season_id=10, episode_id=18, state_serie='utd', user=user)
        s2 = UserMedia(media='serie', media_id=1100, season_id=5, episode_id=6, state_serie='fin', user=user)
        s3 = UserMedia(media='serie', media_id=18347, season_id=5, episode_id=6, state_serie='fin', user=user)
        s4 = UserMedia(media='serie', media_id=4608, season_id=5, episode_id=6, state_serie='utd', user=user)
        user.add_serie(60735)
        user.add_serie(1412)
        user.add_movie(420818)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.add(s4)
        db.session.commit()

        # On verifie que chaque liste possede les deux elements attendus
        self.assertEqual(user.check_upcoming_episodes(),([1668, 4608], [60735, 1412], [1100, 18347]))

    def test_get_notifications(self):
        """
        Ce test verifie la methode get_notifications
        On verifie que la methode ne renvoie que les series qui ne sont pas a jour
        :return: void
        """
        # On cree un utilisateur utilise pendant tout ce test
        TestUser.register(self, 'Username', 'Name', 'Surname', 'test@test.co', 'test@test.co',
                          'password', 'password')

        # On recupere l'utilisateur
        u = User.query.filter_by(name='Name')
        user = u[0]

        # On verifie que la methode marche quand il n'y a pas de series non a jour
        self.assertEqual(user.get_notifications(), [])
        self.assertEqual(user.nb_not_up_to_date(), 0)

        # On lui ajoute des series
        user.add_serie(1412)
        user.add_serie(60735)
        s1 = UserMedia(media='serie', media_id=1668, season_id=10, episode_id=18, state_serie='utd', user=user)
        s2 = UserMedia(media='serie', media_id=1100, season_id=5, episode_id=6, state_serie='fin', user=user)
        user.add_movie(420818)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        # On verifie qu'on n'obtient bien que les deux series non a jour
        self.assertEqual(user.get_notifications(), [('Arrow', 1412), ('The Flash', 60735)])

        # On va egalement tester la methode nb_not_up_to_date
        self.assertEqual(user.nb_not_up_to_date(), 2)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
#


if __name__ == '__main__':
    unittest.main()



