from django.core.management.base import BaseCommand
from polls.models import OilPrice 

class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **kwargs):
        # OilPrice.objects.all().delete()
        all_oil_data = OilPrice.objects.all()
        for data in all_oil_data:
            print(f"Oil Category: {data.oil_category}, Date: {data.date}, Average Price: {data.avg_price}")