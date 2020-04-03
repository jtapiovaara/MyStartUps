import requests
from django.shortcuts import render
from django.views import generic

from .models import Hanke, Yhteys, Etu

# Create your views here.


class HankeLista(generic.ListView):
    model = Hanke

    def hankkeet(self):
        return Hanke.objects.order_by('-nimi')


class YhteysLista(generic.ListView):
    model = Yhteys


class EtuLista(generic.ListView):
    model = Etu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = Hanke.objects.prefetch_related('etu_set')
        context["new_context_entry"] = new_context_entry
        return context


def porssi(request):
    return render(request, 'msu/porssi.html')


def saksanautot(request):
    return render(request, 'msu/saksanautot.html')


def saksanautomyynnit(request, id):

    # Saksassa myytyjen autojen luvut 2017 -2017
    url = 'https://offenedaten.duesseldorf.de/api/action/datastore/search.json?resource_id=9a0b8848-2369-4c05-94c4-550c5990b7f9'

    r = requests.get(url).json()
    # print(id)

    automerkki = int(id)
    tunnus = r['result']['fields'][automerkki]['id']
    # print(tunnus)

    context = {
        'car': tunnus,
        'year0': r['result']['records'][0]['jahr'],
        'sales0': r['result']['records'][0][tunnus],
        'year1': r['result']['records'][1]['jahr'],
        'sales1': r['result']['records'][1][tunnus],
    }

    return render(request, 'msu/saksanautot.html', {'context': context})


def cov19(request):
    url = 'https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData'

    r = requests.get(url).json()
    # print(r)

    vikaalue_act = r['confirmed'][-1]['healthCareDistrict']
    tapausnro_act = r['confirmed'][-1]['id']
    menehtyneet = r['deaths']
    vikaalue_rec = r['recovered'][-1]['healthCareDistrict']
    tapausnro_rec = r['recovered'][-1]['id']


    context = {
        'vikaalue_act': vikaalue_act,
        'tapausnro_act': tapausnro_act,
        'menehtyneet': menehtyneet,
        'vikaalue_rec': vikaalue_rec,
        'tapausnro_rec': tapausnro_rec,
    }

    return render(request, 'msu/cov19.html', {'context': context})




