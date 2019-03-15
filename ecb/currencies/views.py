from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Currency, History


def index(request):
    currencies = Currency.objects.all()
    context = {'currencies': currencies}
    return render(request, 'currencies/index.html', context)


def history(request, currency_id):
    history = get_list_or_404(History.objects.filter(currency_id=currency_id).order_by('-pub_date'))
    return render(request, 'currencies/history.html', {'history': history})
