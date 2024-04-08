from flask_mail import Message

def mailsender(recipient, username):
    from app import mail
    print("  inside mail sending   ")
    name = "buvanesh"
    msg = Message(
        'Hi {},'.format(name),
        sender='20p308@kce.ac.in',
        recipients=[recipient]
    )
    msg.body = '''Hi {},\n''' \
               '''{} wants to follow you.\n'''.format(name, username)
    mail.send(msg)
    return 'Sent'
