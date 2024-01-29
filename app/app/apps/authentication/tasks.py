import time

from celery import shared_task, chain

from .models import User 

from utils.email import email_new_user, email_welcome_user


@shared_task
def send_email_new_user(username, email, created_at_isoformat, with_welcome=False):
    time.sleep(5)
    email_new_user(username, username, email, created_at_isoformat)
    if with_welcome:
        send_email_welcome.delay(username, email)

@shared_task
def send_email_welcome(username, email):
    time.sleep(0.5)
    email_welcome_user(username, username, email)

@shared_task
def join_mail_new_welcome_user(id_user):
    try:
        user = User.objects.get(pk=id_user)
        task_email_new_user = send_email_new_user.si(user.username, user.email, user.created_at.isoformat()).set(countdown=2)
        chain(
            task_email_new_user, 
            send_email_welcome.si(user.username, user.email).set(countdown=4)
        )()
    except User.DoesNotExist:
        print(f"User doesn't exist")
    except Exception as e:
        print(f"error: {e}")
