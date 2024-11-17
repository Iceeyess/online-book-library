#  CONSTANTS:
########################################################################
TAX_20_VALUE = 0.2  # 20% of revenue
########################################################################


def return_book_back(view_object):
    """This service function gets back Rent object and put books back into library, id est book attribute
    'is_available' marks as True"""
    if not view_object.are_books_returned:
        view_object.are_books_returned = True
        for book in view_object.books:
            book.is_available = True
        view_object.save()
    return view_object