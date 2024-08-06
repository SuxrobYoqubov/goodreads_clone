from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser

# email jo'natish------------------------------------

@receiver(post_save, sender = CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
                "Welcome to Goodreads Clone",
                f"Hi, {instance.username}. Welcome to Goodreads clone. Enjoy the books and reviews.",
                "yoqubovsuxrob1999@gmail.com",
                [instance.email],

           )