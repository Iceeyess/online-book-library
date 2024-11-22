from django.core.mail import send_mail

from books.models import Rent
from config.settings import EMAIL_HOST_USER

#CONSTANTS:
########################################################################
TAX_20_VALUE = 20 / 120  # 20% of revenue
########################################################################


def return_book_back(view_object) -> Rent:
    """This service function gets back Rent object and put books back into library, id est book attribute
    'is_available' marks as True"""
    if not view_object.are_books_returned:
        view_object.are_books_returned = True
        view_object.save()
        for book in view_object.books.all():
            book.is_available = True
            book.save()
    return view_object

def sending_email(obj) -> None:
    """This function sends an email to renters"""
    subject = 'Book return confirmation'
    message = (f'Dear {obj.username.username},'
               f'\n\nYour book return request has been successfully processed. Your rental '
               f'period will be extended until {obj.deadline}.\n\n'
               f'Please consider for soon meet a library to proceed with book returning.\n\n'
               f'with regards,\n'
               f'Library administration.')
    email_from = EMAIL_HOST_USER
    recipient_list = [obj.username.email]
    send_mail(subject, message, email_from, recipient_list)