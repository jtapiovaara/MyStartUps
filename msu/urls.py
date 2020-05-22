from django.urls import path
from . import views
from msu.views import MunView

# app_name = 'msu'

urlpatterns = [
    path('', views.HankeLista.as_view(), name='hanke'),
    path('yhteys/', views.YhteysLista.as_view(), name='yhteys'),
    path('etu/', views.EtuLista.as_view(), name='etu'),
    path('sijainti/', views.SijaintiLista.as_view(), name='sijainti'),
    path('mine/', MunView.as_view(), name='mun-view'),
    path('porssi/', views.porssi, name='porssi'),
    path('saksanautot/', views.saksanautot, name='saksanautot'),
    path('saksanautomyynnit/<id>', views.saksanautomyynnit, name='saksanautomyynnit'),
    path('cov19/', views.cov19, name='cov19'),
    path('pie-chart/', views.pie_chart, name='pie-chart'),
]