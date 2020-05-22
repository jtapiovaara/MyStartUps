from django.contrib import admin

from .models import Hanke, Yhteys, Etu, Sijainti


class SijaintiAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Postinumero',               {'fields': ['posti_numero']}),
        ('Paikka',               {'fields': ['paikka']}),
        ('Osavaltio',               {'fields': ['osavaltio']}),
        ('Latitude',               {'fields': ['lat']}),
        ('Longitude',               {'fields': ['lon']}),
    ]
    list_display = ('posti_numero', 'paikka')
    search_fields = ['posti_numero', 'osavaltio']


admin.site.register(Hanke)
admin.site.register(Yhteys)
admin.site.register(Etu)
admin.site.register(Sijainti, SijaintiAdmin)