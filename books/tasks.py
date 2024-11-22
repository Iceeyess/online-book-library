from datetime import datetime
from celery import shared_task
from books.models import Rent
from .services import sending_email


@shared_task
def checking_expires():
    """This task is scheduled to run every day.
    It checks the expiration date of rentals and sends an email to renters if the rental period is over."""
    rents = Rent.objects.filter(deadline__lt=datetime.now())
    for i, rent in enumerate(rents, start=1):
        print(i, rent)
        sending_email(rent)
