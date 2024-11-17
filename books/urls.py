from books import views
from books.apps import BooksConfig
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = BooksConfig.name

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='books')
router.register(r'authors', views.AuthorViewSet, basename='authors')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'rent', views.RentViewSet, basename='rent')
urlpatterns = [
    path('rent/return/<int:pk>/', views.ReturnBackBookUpdateAPIView.as_view(), name='return-book')
] + router.urls