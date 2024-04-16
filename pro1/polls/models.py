from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=10)
    deal_bas_r = models.FloatField()
    search_date = models.DateTimeField()

    def __str__(self):
        return self.cur_unit

class OilPrice(models.Model):
    date = models.DateField()
    oil_category = models.CharField(max_length=100)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2)