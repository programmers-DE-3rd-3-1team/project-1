from django.http import JsonResponse
from django.shortcuts import render
from .models import ExchangeRate

def get_data(request):
    data = list(ExchangeRate.objects.values('cur_unit', 'deal_bas_r', 'search_date'))
    return JsonResponse(data, safe=False)

def index(request):
    items = ExchangeRate.objects.all()
    return render(request, 'index.html', {'items': items})
