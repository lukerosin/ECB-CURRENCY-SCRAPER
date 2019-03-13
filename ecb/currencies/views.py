from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Currency, History


def index(request):
    currency_list = Currency.objects.all()
    context = {'currency_list': currency_list}
    return render(request, 'currencies/index.html', context)


def history(request, name):
    rate_list = get_list_or_404(History, pk=name)
    return render(request, 'currencies/history.html', {'rate': rate_list})