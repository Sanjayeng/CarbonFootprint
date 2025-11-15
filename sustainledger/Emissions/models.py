from django.db import models


class EmissionFactor(models.Model):
    category = models.CharField(max_length=100)      
    factor_value = models.FloatField()               
    unit = models.CharField(max_length=50)           

    def __str__(self):
        return f"emissionfactor {self.id} {self.category}"


class Activity(models.Model):
    core = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=100)
    value = models.FloatField()                     
    date = models.DateField()                       

    def __str__(self):
        return f"activity {self.id} {self.category}"

class ConvertedEmission(models.Model):
    activity = models.CharField(max_length=255)
    co2e_value = models.FloatField(null=True, blank=True)
    emission_factor = models.CharField(max_length=255, null=True, blank=True)  
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.co2e_value)

