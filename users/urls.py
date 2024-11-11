from django.urls import path
from rest_framework import routers
from . import views
from .apps import UsersConfig
from .views import MyTokenObtainPairView

app_name = UsersConfig.name

router = routers.SimpleRouter()
router.register(r'', views.UsersViewSet, 'user')

urlpatterns = [
    # Obtain token
    path('token/', MyTokenObtainPairView.as_view(), name='token-obtain-pair')
] + router.urls
