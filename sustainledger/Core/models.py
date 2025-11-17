from django.db import models

class Core(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        
        return f'core {self.id}{self.name}' #self.name


class Facility(models.Model):
    core = models.ForeignKey(Core, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.core.name})"
    
    