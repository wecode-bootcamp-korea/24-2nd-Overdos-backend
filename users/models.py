from django.db import models

class User(models.Model):
    name = models.CharField(max_length=60)
    social_id = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=50)

    class Meta:
        db_table='users'
