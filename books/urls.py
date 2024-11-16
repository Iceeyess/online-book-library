from books import views
from books.apps import BooksConfig
from rest_framework.routers import SimpleRouter, DefaultRouter
from django.urls import path, include

app_name = BooksConfig.name

router = DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'authors', views.AuthorViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'rent', views.RentViewSet)
urlpatterns = [
] + router.urls