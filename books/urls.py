from books import views
from books.apps import BooksConfig
from rest_framework.routers import SimpleRouter


app_name = BooksConfig.name

router1 = SimpleRouter()
router1.register(r'authors', views.AuthorViewSet, basename='author')
router2 = SimpleRouter()
router2.register(r'genres', views.GenreViewSet, basename='genre')
router3 = SimpleRouter()
router3.register(r'', views.BookViewSet, basename='book')
router4 = SimpleRouter()
router4.register(r'rent', views.RentViewSet, basename='rent')

urlpatterns = [

] + router1.urls + router2.urls + router3.urls + router4.urls

