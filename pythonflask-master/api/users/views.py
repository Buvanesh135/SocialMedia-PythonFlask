from app import mail
from flask import Blueprint
from factory import create_app
from flask_mail import Message
# app,mail=create_app(__name__)

def mailsender(recipient,username):
            name="buvanesh"
            msg = Message(
                'Hi {} ,'.format(name),
                sender='20p308@kce.ac.in',
                recipients=[recipient]
            )
            msg.body = '''Hi {},\n''' \
                       '''{} wants to follow you.\n''' \
                       . format(name,username)
            mail.send(msg)
            return 'Sent'