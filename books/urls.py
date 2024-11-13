from books import views
from books.apps import BooksConfig
from rest_framework.routers import SimpleRouter


app_name = BooksConfig.name

router = SimpleRouter()
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'', views.BookViewSet, basename='book')
router.register(r'rent', views.RentViewSet, basename='rent')

urlpatterns = [

] + router.urls

