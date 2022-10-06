from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Create your models here.


class Employee(models.Model):

    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, blank=False, unique=True, validators=[validate_email])

class Events(models.Model):

    summary = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()