from django.urls import path
from . import views

urlpatterns = [
    path('', views.HankeLista.as_view(), name='hanke'),
    path('yhteys/', views.YhteysLista.as_view(), name='yhteys'),
    path('etu/', views.EtuLista.as_view(), name='etu'),
    path('porssi/', views.porssi, name='porssi'),
    path('saksanautot/', views.saksanautot, name='saksanautot'),
    path('saksanautomyynnit/<id>', views.saksanautomyynnit, name='saksanautomyynnit'),
    path('cov19/', views.cov19, name='cov19')
]