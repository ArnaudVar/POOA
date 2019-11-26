from flask_mail import Message
from app import mail,app
from flask import render_template
from threading import Thread

'''
Ce .py sert à gérer toute la partie envoie de mail de notre application. 
La seule utilisation actuelle est l'envoi de mail pour reset son password
'''

def send_async_email(app, msg):
    '''
    Méthode utilisée pour envoyer des emails de manière asynchrone grâce à un thread
    :param app: package python, notre app
    :param msg: un objet Message : le mail a envoyer
    :return: Void
    '''
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    '''
    Méthode utilisée pour appeler la méthode send_async_email pour envoyer un mail
    :param subject: l'objet du mail
    :param sender: l'émetteur du mail
    :param recipients: les destinataires du mail
    :param text_body: Le texte du mail
    :param html_body: L'html du mail
    :return: Void
    '''
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_password_reset_email(user):
    '''
    Méthode utilisée pour envoyer un mail de reset de password à un utilisateur
    :param user: Un objet user : l'utilisateur a qui envoyer le mail
    :return: Void
    '''
    token = user.get_reset_password_token()
    send_email('[SeryeGenda] Reset Your Password',
               sender=app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
