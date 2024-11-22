from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


NULLABLE = dict(null=True, blank=True)


class User(AbstractUser):
    """Overridden class for users, added below attributes"""
    email = models.EmailField(unique=True, help_text='Email address', **NULLABLE)
    image = models.ImageField(upload_to='photo/users/', help_text='Image', **NULLABLE)
    phone = models.CharField(default=None, max_length=50, help_text='Phone number', **NULLABLE)
    city = models.CharField(max_length=50, help_text='City name', **NULLABLE)
    street = models.CharField(max_length=50, help_text='Street name', **NULLABLE)
    house_number = models.CharField(max_length=10, help_text='House number', **NULLABLE)
    apartment_number = models.CharField(max_length=10, help_text='Apartment number', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __repr__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('pk', )
