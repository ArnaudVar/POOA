from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask import request


class LoginForm(FlaskForm):
    """
    Cette classe permet l'implemenation du login des utilisateurs
    Elle heriete de la class FlaskForm du module flask_wtf

    Ces doivent rentrer un username non vide, un mot de passe non vide et
    ont l'option de choisir de ne pas se reconnecter pendant 1 h (dans les parametres du projet)
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SearchForm(FlaskForm):
    """
    Cette classe nous permet d'effectuer une recherche dans le site
    Elle herite de la classe FlaskForm du module flask_wtf

    Le formulaire ne contient qu'un champ
    """
    s = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class RegistrationForm(FlaskForm):
    """
    Cette classe herite de la classe FlaskForm du module flask_wtf
    Elle permet l'implementation de l'enregistrement d'un nouvel utilisateur

    On y prend toutes ses informations. On lui demande de saisir 2 fois son email et son mot de passe pour etre
    sur qu'il n'y a pas d'erreurs dans ces derniers
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    email2 = StringField('Repeat Email', validators=[DataRequired(), EqualTo('email')])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Cette methode nous permet de verifier que le nom d'utilisateur choisi par l'utilisateur n'est pas deja pris
        :param username: string
        :return:
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already used, please use a different username.')

    def validate_email(self, email):
        """
        Cette methode nous permet de verifier que l'email entre par l'utilisateur n'est pas deja pris
        :param email: email string
        :return:
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This e-mail is already used, please use a different email address.')


class ResetPasswordRequestForm(FlaskForm):
    """
    Cette classe permet l'implementation d'un formulaire permettant de demander un changement de mot de passe
    On y demande un email
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    """
    Cette classe permet a l'utilisateur de changer son mot de passe apres avoir recu le mail de reinitialisation
    """
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
