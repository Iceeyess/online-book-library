from django.utils import timezone
from celery import shared_task
from books.models import Rent
from .services import sending_email


@shared_task
def checking_expires():
    """This task is scheduled to run every day.
    It checks the expiration date of rentals and sends an email to renters if the rental period is over."""
    rents = Rent.objects.filter(deadline__lt=timezone.now(), are_books_returned=False)
    for rent in rents:
        sending_email(rent)
