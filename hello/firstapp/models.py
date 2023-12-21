from django.db import models

class Event (models. Model):
    type = models.TextField()
    title = models.TextField()
    image = models.ImageField(upload_to='hello/static/photos')
    data = models.TextField()
    org = models.TextField()

    class Meta:
        db_table = 'event'

class Users(models.Model):
    number = models.TextField() 
    Full_name = models.TextField() 
    gender = models.CharField(max_length=10)
    type = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    direction = models.TextField() 
    event = models.TextField()
    image = models.ImageField(upload_to='hello/static/photos')

    class Meta:
        db_table = 'users'

class Post:
    pass

