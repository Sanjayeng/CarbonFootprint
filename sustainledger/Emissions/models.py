from django.db import models
from Core.models import Facility

class EmissionFactor(models.Model):
    category = models.CharField(max_length=100)
    factor_value = models.DecimalField(max_digits=10, decimal_places=6)
    unit = models.CharField(max_length=50)


class Activity(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=50)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.facility.name} - {self.category}"


class ConvertedEmission(models.Model):
    activity = models.ForeignKey("Emissions.Activity", on_delete=models.CASCADE)
    co2e_value = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.SET_NULL, null=True, blank=True)
    calculated_at = models.DateTimeField(auto_now_add=True)
