import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic, View

from .models import Hanke, Yhteys, Etu, Sijainti

# Create your views here.


class HankeLista(generic.ListView):
    """Omat StartUP -hankkeeni"""
    model = Hanke

    def hankkeet(self):
        return Hanke.objects.order_by('-nimi')

    def ajat(self):
        return Hanke.objects.order_by('-aika')

    def arvot(self):
        return Hanke.objects.order_by('-etu__arvo')


class YhteysLista(generic.ListView):
    """StartUP -hankkeitteni yhteyshenkilöitä"""
    model = Yhteys


class EtuLista(generic.ListView):
    """Saavutettuja ja toteutuneita etuja (perks) StartUp -osallistumisistani.
    Kiinnostava "get_context_data" kokeilussa"""
    model = Etu

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = Hanke.objects.prefetch_related('etu_set').order_by('etu__arvo')
        context["new_context_entry"] = new_context_entry
        return context


class SijaintiLista(generic.ListView):
    """Listalle Django Admin  (tai Vue) kautta päivitetyt Yhdysvaltalaiset postinumerot"""
    model = Sijainti


class MunView(View):
    """Tämä on rakennettu, jotta voin harjoitella ja ymmärtää miten Djangon view -osastot toimivat.
    Ihan perusview, siis 'view' toimii kokonaan ilman mitään renderöintejä, palauttaen vain HttpResponsen."""

    def get(self, request):
        return HttpResponse(
            '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">'
            '<div class="container">'
            '<h2> No Template is fine also </h2>'
            'Tämähän menee tyylikkäästi näinkin.  Kirjoitettuna suoraan views.py -tiedostoon.'
            ' Jos tämä menisi vain näillä staattisilla, niin koko paketin voisi kirjoittaa suoraan Pythonilla.'
            '<p>Django HttpResponse jyrää.</p>'
            '<hr>'
            '<h3>Vaikkapa tyylikkäästi muotoiltu taulukko</h3>'            
            '<table class="table">'
            '<thead>'
            '<tr>'
            '<th>Etunimi</th>'
            '<th>Sukunimi</th>'
            '<th>Email</th>'
            '</tr>'
            '</thead>'
            '<tbody>'
            '<tr>'
            '<td>Jouni</td>'
            '<td>Tapiovaara</td>'
            '<td>jtapiovaara@gmail.com</td>'
            '</tr>'
            '<tr>'
            '<td>Ruben</td>'
            '<td>Stibu</td>'
            '<td>rs@example.com</td>'
            '</tr>'
            '</tbody>'
            '</table>'
            '<hr>'
            '<h3>Tai Bootstrapin muokkaama description list</h3>'
            '<h4>Kuvailulista</h4>'
            '<p>The dl element indicates a description list:</p>'
            '<dl>'
            '<dt>Kahvi</dt>'
            '<dd>- kuuma, musta juoma</dd>'
            '<dt>Maito</dt>'
            '<dd>- kylmä, valkoinen juoma</dd>'
            '<dt>Kaurajuoma</dt>'
            '<dd>- kylmä, moderni juoma</dd>'
            '</dl>'
            '<hr>'
            '</div>'
        )


def pie_chart(request):
    """charts.js kirjaston käyttöönotto. Haetaan kustannusjärjestyksessä (rank) kaikki start-upit
     ja lähetetään ne templateen, jossa scripti tekee työnsä. Hieman rumuutta tulee siitä, että Djangon
     kaarisulku -viitausta käytetään JS sisällä.  Ei tulisi, eikä saisi, mutta kun tiesi mitä tekee,
     niin näinkin käy.  Tulos ratkaisee. Nimi on pie-chart, mutta esitys on bar-chart."""
    labels = []
    data = []

    queryset = Etu.objects.all().order_by('rank')
    for etu in queryset:
        labels.append(etu.nimi)
        data.append(etu.arvo)

    return render(request, 'msu/pie_chart.html', {
        'labels': labels,
        'data': data
            })


def porssi(request):
    """Omien osakkeiden kurantti tilanne.  Manuaalinen "tyhmä" toteutus toistaiseksi"""
    return render(request, 'msu/porssi.html')


def saksanautot(request):
    """Saksan Dusseldorfin alueen autokauppiaiden myyntitilastot vuosilta 2017 ja 2018.
    Funktio avaa sivuston, ei muuta"""
    return render(request, 'msu/saksanautot.html')


def saksanautomyynnit(request, id):
    """Saksan Dusseldorfin alueen autokauppiaiden myyntitilastot vuosilta 2017 ja 2018.  Esitetään tarkemmat
    myyntitiedot valitusta automerkistä ja lisäksi osoitetaan ao. merkkiä edustavat kauppiaat GoogleMaps -scriptillä.
    url-linkistä parsitaan tiedot json -muotoon ja poimitaan halutut mukaan renderöitävään sivuun. Cool."""

    # Saksassa myytyjen autojen luvut 2017 - 2018
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
    """Tämä funktio toimi virus-pandemian alkuaikoina, mutta päivittäminen väheni.
    Haetaan avoimesta rajapinnasta Amazonilla tietoja kaksitasoisesta JSON--rakenteesta ja esitetään ne.
    Muutoin staattiset toiminnot, ei argumentteja"""
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







