from django.db import models

# Create your models here.

class Entry(models.Model):

    class Condition(models.IntegerChoices):
        NA   = 0, 'N/A'
        GOOD = 3, 'Good'
        FAIR = 2, 'Fair'
        POOR = 1, 'Poor'

    date      = models.DateTimeField(auto_now_add=True)
    user      = models.CharField(max_length=150)
    battery   = models.CharField(max_length=3)
    ready     = models.BooleanField(null=True)
    condition = models.PositiveSmallIntegerField(choices=Condition.choices, default=Condition.NA, null=True)
    charge    = models.DecimalField(max_digits=4, decimal_places=1, null=True)
    rint      = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    memo      = models.TextField(null=True)