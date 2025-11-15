from django.db import models

# Create your models here.
class core (models.Model):
    name = models.CharField(max_length=100)
    location= models.TextField()

    def __str__(self):
        return f'core {self.id}: {self.name}' #self.name 
