from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=10)
    deal_bas_r = models.FloatField()
    search_date = models.DateTimeField()

    def __str__(self):
        return self.cur_unit