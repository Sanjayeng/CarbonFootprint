from django.db import models
from Core.models import core

# Create your models here.
from django.db import models
from Core.models import core

class EmissionFactor(models.Model):
    CATEGORY_CHOICES = (
        ('electricity', 'Electricity'),
        ('fuel', 'Fuel'),
        ('travel', 'Travel'),
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    factor_value = models.DecimalField(max_digits=10, decimal_places=6)  # e.g. 0.000475
    unit = models.CharField(max_length=50)  # e.g. 'tCO2e per kWh'

    def __str__(self):
        return f"{self.category} - {self.factor_value} {self.unit}"


class Activity(models.Model):
    CATEGORY_CHOICES = (
        ('electricity', 'Electricity'),
        ('fuel', 'Fuel'),
        ('travel', 'Travel'),
    )

    facility = models.ForeignKey(core, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)  # kWh, liters, km
    date = models.DateField()

    def __str__(self):
        return f"{self.facility} - {self.category} - {self.value}"


class ConvertedEmission(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)
    co2e_value = models.DecimalField(max_digits=12, decimal_places=6)
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.SET_NULL, null=True)
    calculated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.co2e_value} tCO2e"
