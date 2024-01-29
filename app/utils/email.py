from django.core.mail import EmailMessage
from django.conf import settings

def _send_email(subject, body, lst_destinatario, bcc=None,):
    if type(lst_destinatario)==str:
        lst_destinatario = [lst_destinatario]
    elif type(lst_destinatario)==list:
        pass
    else:
        raise ValueError("Email should be a str or list")
    
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=lst_destinatario,
        bcc=bcc,
    )

    email.send(fail_silently=False)


def email_new_user(full_name, username,email_user, date_joined):
    body = """
        Nuevo Usuario: """+full_name+"""
        Con email: """+email_user+"""
        Con Username: """+username+"""
        Con fecha: """+date_joined+"""
    """
    try:
        _send_email("Nuevo usuario,", body, email_user)

    except Exception as e:
        print( "Exception ",str(e))


def email_welcome_user(full_name, username,email_user):
    body = """
        Nuevo Usuario: """+full_name+"""
        Con email: """+email_user+"""
        Con Username: """+username+"""
        Welcome to bussness
    """
    try:
        _send_email("Welcome new user,", body, email_user)

    except Exception as e:
        print( "Exception ",str(e))
