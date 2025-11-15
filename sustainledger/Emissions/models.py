from django.db import models


class Activity(models.Model):
    core = models.CharField(max_length=100, default="Unknown")

    category = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()


class EmissionFactor(models.Model):
    category = models.CharField(max_length=100)
    factor_value = models.DecimalField(max_digits=10, decimal_places=6)
    unit = models.CharField(max_length=50)


class ConvertedEmission(models.Model):
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE)
    co2e_value = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.SET_NULL, null=True, blank=True)
    calculated_at = models.DateTimeField(auto_now_add=True)
