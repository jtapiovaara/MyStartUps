import requests

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.http import HttpResponse, request
from django.views import generic, View
from django.db.models import Sum

from .models import Hanke, Yhteys, Etu, Sijainti
from .forms import HankeDetailForm
from MyStartUps.ei_gittiin import TRELLOSTA_API_SECRET, TRELLO_IDLIST, NASA_API_KEY, GOLF_KEY, TRELLOSTA_API_KEY

from trello import TrelloClient, Card

# Create your views here.


class HankeLista(generic.ListView):
    """Omat StartUP -hankkeeni"""
    model = Hanke

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hankkeet'] = Hanke.objects.order_by('-nimi')
        context['ajat'] = Hanke.objects.order_by('-aika')
        context['arvot'] = Hanke.objects.order_by('-etu__arvo')
        context['summa'] = Etu.objects.aggregate(Sum('arvo'))
        return context


class HankeDetail(generic.DetailView):
    model = Hanke


class YhteysLista(generic.ListView):
    """StartUP -hankkeitteni yhteyshenkilöitä. prefetch_related -haku."""
    model = Yhteys

    # def yhteydet(self):
    #     return Yhteys.objects.filter(pk__in=[1, 2, 4])
    #
    # def varalla(self):
    #     return Hanke.objects.prefetch_related('yhteys_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['yhteydet'] = Yhteys.objects.filter(pk__in=[1, 2, 4])
        context['varalla'] = Hanke.objects.prefetch_related('yhteys_set')
        return context


class EtuLista(generic.ListView):
    """Saavutettuja ja toteutuneita etuja (perks) StartUp -osallistumisistani.
    Kiinnostava "get_context_data" kokeilussa. select_related -haku. Huomaa myös, get_context_data vs. oma funktio.
    Kun ei käytä "get-cont..." niin kantaan tehdään tietty haku aina, toisin kuin kontekstissa tieto
    haettaisiin vain kerran."""
    model = Etu

    def rankki(self):
        return Etu.objects.order_by('rank')

    def new_context_entry(self):
        return Hanke.objects.select_related().order_by('-etu__arvo')


class SijaintiLista(generic.ListView):
    """Listalle Django Admin kautta päivitetyt Yhdysvaltalaiset postinumerot. Avain haetaan ympäristömuuttujasta.
    API toimii parhaiten, jos mukaan laittaa päivämäärän esim. date=2020-10-10. Ilman päivämäärääkinkin toimii."""
    model = Sijainti

    #TODO api toimii parhaiten, jos antaa päivämäärän. Se on nyt hardcoded templatessa. Voisi pyytää käyttäjältä myös.

    def nasakey(self):
        nasakey = NASA_API_KEY
        return nasakey


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
            '<th class="text-primary">Etunimi</th>'
            '<th class="text-info">Sukunimi</th>'
            '<th class="text-danger">Site</th>'
            '</tr>'
            '</thead>'
            '<tbody>'
            '<tr>'
            '<td>Jouni</td>'
            '<td>Tapiovaara</td>'
            '<td><a href="http://www.jtamefiles.fi/projektit" target = _blank > My Site <a></td>'
            '</tr>'
            '<tr>'
            '<td>Ruben</td>'
            '<td>Stibu</td>'
            '<td>rs@example.com</td>'
            '</tr>'
            '</tbody>'
            '</table>'
            '<hr>'
            '<h3>Tai Bootstrapin muokkaama TODO list</h3>'
            '<h4>Tehtävälista</h4>'
            '<p>These yoy need to get today:</p>'
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

    automerkki = int(id)
    tunnus = r['result']['fields'][automerkki]['id']

    context = {
        'car': tunnus,
        'year0': r['result']['records'][0]['jahr'],
        'sales0': r['result']['records'][0][tunnus],
        'year1': r['result']['records'][1]['jahr'],
        'sales1': r['result']['records'][1][tunnus],
    }

    return render(request, 'msu/saksanautot.html', {'context': context})


def cov19(request):
    form = HankeDetailForm()
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
        'form': form,
        'vikaalue_act': vikaalue_act,
        'tapausnro_act': tapausnro_act,
        'menehtyneet': menehtyneet,
        'vikaalue_rec': vikaalue_rec,
        'tapausnro_rec': tapausnro_rec,
    }

    return render(request, 'msu/cov19.html', {'context': context})


def spacex(request):
    """Open Source REST API for rocket, core, capsule, pad, and launch data, created and maintained by the
    developers of the r/SpaceX organization. Erittäin kiinnostava rajapinta.
    Voisi lisätä raportoinnin esim. Näytä huippuhetket: eka ok, eka dronelanding, starman, dragon etc. Näytä Starlinks.
    Näytä eri kaupalliset asiakkaat valikolla. Näytä sotilaslennot. Myös ISS miehitystiedot (ei virallinen)."""

    astronautti_url = 'http://api.open-notify.org/astros.json'

    a = requests.get(astronautti_url).json()

    astronautti = a['number']

    url = 'https://api.spacexdata.com/v2/launches'
    #FIXME this url may or may not be the latest one. control.

    r = requests.get(url).json()
    latest_flight = r[-1]['flight_number']
    number_of_flights = int(latest_flight)

    # mission_names = []
    # mission_name_counter = int(0)
    # while mission_name_counter < number_of_flights:
    #     # print(r[mission_name_counter]['mission_name'])
    #     mission_names.append(r[mission_name_counter]['mission_name'])
    #     mission_name_counter = mission_name_counter + 1

    # allstarlink = r__contains = "Starlink"
    # allstarlink = r.get(r[99]['mission_name']=="Starlink-10 (v1.0) & SkySat 19-21")
    # print(allstarlink)

    mission_data = []
    counter = int(0)

    while counter < number_of_flights:
        # failed_count = int(0)
        # if r['launch_success'] is ['False']:
        #     failed = failed_count + 1

        data = {
            'mission_name': r[counter]['mission_name'],
            'flight_number': r[counter]['flight_number'],
            'mission_patch_small': r[counter]['links']['mission_patch_small'],
            'launch_success': r[counter]['launch_success'],
            'launch_year': r[counter]['launch_year'],
            'video': r[counter]['links']['video_link'],
        }
        mission_data.append(data)
        counter = counter+1

    # print(failed)

    context = {
        'astronautti': astronautti,
        'latest_flight': latest_flight,
        'mission_data': mission_data,
    }

    return render(request, 'msu/spacex.html', {'context': context})


def spacexdetail(request, flight_number):
    url = 'https://api.spacexdata.com/v2/launches'
    r = requests.get(url).json()
    flight = int(flight_number)-1
    # print(flight)

    this_flight = r[flight]
    launch_date = r[flight]['launch_date_utc'][:10]
    # print(launch_date)

    context = {
        'launch_date': launch_date,
        'this_flight': this_flight,
    }
    # print(this_flight)

    return render(request, 'msu/spacexdetail.html', {'context': context})


def glowit(request):
    """Coolit hehkuvat efektit painonappeihin (#codepen.io)"""
    return render(request, 'msu/glowing.html')


def tiger(request):
    """Golf Player data in PGA Statistics. Tiger Woods 40000019, Bubba Watson 40000001"""
    # List of all Players:
    # https://api.sportsdata.io/golf/v2/json/Players?key=d519d3b3e7b340e18a8b2959c6ee1eda
    # List of coming Tournaments:
    # https://api.sportsdata.io/golf/v2/json/Tournaments?key=d519d3b3e7b340e18a8b2959c6ee1eda
    # List of current years Tournaments (give year)
    # https://api.sportsdata.io/golf/v2/json/Tournaments/2020?key = d519d3b3e7b340e18a8b2959c6ee1eda

    url = 'https://api.sportsdata.io/golf/v2/json/Player/40000019?key='+GOLF_KEY

    r = requests.get(url).json()

    PlayerID = r['PlayerID']
    FirstName = r['FirstName']
    LastName = r['LastName']
    Swings = r['Swings']
    Photo = r['PhotoUrl']
    College = r['College']
    BirthCity = r['BirthCity']
    BirthState = r['BirthState']
    BirthDate = r['BirthDate']

#     "Weight": 185,
#     "PgaDebut": 1992,
#     "SportRadarPlayerID": "d74e6369-dcb4-4225-8152-90d3f19d2517",
#     "PgaTourPlayerID": 8793,
#     "RotoworldPlayerID": 102,
#     "RotoWirePlayerID": null,
#     "FantasyAlarmPlayerID": null,
#     "DraftKingsName": "Tiger Woods",
#     "FantasyDraftName": "Tiger Woods",
#     "FanDuelName": "Tiger Woods",
#     "FantasyDraftPlayerID": 254312,
#     "DraftKingsPlayerID": 1594,
#     "FanDuelPlayerID": 78999,
#     "YahooPlayerID": 147
#
#
    context = {
        'PlayerID': PlayerID,
        'FirstName': FirstName,
        'LastName': LastName,
        'Swings': Swings,
        'Photo': Photo,
        'College': College,
        'BirthCity': BirthCity,
        'BirthState': BirthState,
        'BirthDate': BirthDate,
    }

    return render(request, 'msu/tiger.html', {'context': context})


def trellostatrelloon(request):
    client = TrelloClient(
        # api_key=api_key,
        api_key=TRELLOSTA_API_KEY,
        api_secret=TRELLOSTA_API_SECRET,
        # token='your-oauth-token-key',
        # token_secret='4b70b7d95e6b2ab54985a631f4dc54ae03cc92e4a4414e88a881d1176c7c5d83'
    )
    all_boards = client.list_boards()
    for index, value in enumerate(all_boards):
        print(f'{index}: {value}')

    my_board = all_boards[1]
    # print(my_board)
    my_startup_list = my_board.list_lists()[1]
    # my_startup_list = my_list[-1]
    # print(my_startup_list.id)
    # my_list = last_board.get_list(list_id)
    # for card in last_board.list_lists():
    #     print(card.name)

    context = {
        'my_startup_list': my_startup_list,
        'my_board': my_board,
    }

    return render(request, 'msu/trelloapi.html', context)


def uusitrellokortti(request):
    url = "https://api.trello.com/1/cards"

    uusi_kortti = 'Uusi kortti'

    key = 'TRELLOSTA_API_KEY'
    token = 'TRELLOSTA_API_SECRET'
    idlist = 'TRELLO_IDLIST'

    query = {
        'key': key,
        'token': '114e9eee2808fcc9db3fc43839bfb51013dd27e5abc28bd55cafca6492cd54f3',
        'idList': idlist,
        'name': uusi_kortti,
    }

    response = requests.request(
        "POST",
        url,
        params=query,
    )
    print(response.status_code)
    context = {
        'name': uusi_kortti,
    }

    return render(request, 'msu/uusitrello.html', context)


def uusitrellolista(request):

    listat = ['eka', 'toka', 'kolmas']
    context = enumerate(listat)
    for index, value in context:
        print(f'{index}: {value}')

    return render(request, 'msu/uusitrellolista.html')
