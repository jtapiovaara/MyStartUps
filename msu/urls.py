from django.urls import path
from . import views
from msu.views import MunView

# app_name = 'msu'

urlpatterns = [
    path('', views.HankeLista.as_view(), name='hanke'),
    path('detail/<int:pk>/', views.HankeDetail.as_view(), name='detail'),
    path('yhteys/', views.YhteysLista.as_view(), name='yhteys'),
    path('etu/', views.EtuLista.as_view(), name='etu'),
    path('sijainti/', views.SijaintiLista.as_view(), name='sijainti'),
    path('mine/', MunView.as_view(), name='mun-view'),
    path('porssi/', views.porssi, name='porssi'),
    path('saksanautot/', views.saksanautot, name='saksanautot'),
    path('saksanautomyynnit/<id>', views.saksanautomyynnit, name='saksanautomyynnit'),
    path('cov19/', views.cov19, name='cov19'),
    path('spacex/', views.spacex, name='spacex'),
    path('spacex/<flight_number>', views.spacexdetail, name='spacexdetail'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
    path('hehkutusta/', views.glowit, name='glowit'),
    path('tiger/', views.tiger, name='tiger'),
    path('trelloapi/', views.trellostatrelloon, name='trelloapi'),
    path('uusitrello/', views.uusitrellokortti, name='uusitrello'),
    path('uusitrellolista/', views.uusitrellolista, name='uusitrellolista')
]