from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

GENDERS = (
    ('male', 'Erkak'),
    ('female', 'Ayol'),
)
class CustomUser(AbstractUser):

    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDERS, verbose_name="Jinsi")
    photo = models.ImageField(upload_to='users/img',blank=True,null=True)
    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse('home')


