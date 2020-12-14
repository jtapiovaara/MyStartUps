from django.db import models
import requests

# Create your models here.


class Hanke(models.Model):
    nimi = models.CharField(max_length=32)
    tyyppi = models.CharField(max_length=32, blank=True)
    miksi = models.TextField(blank=True)
    tavoite = models.TextField(blank=True)
    aika = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.nimi

    class Meta:
        ordering = ('nimi',)


class Yhteys(models.Model):
    etunimi = models.CharField(max_length=64, blank=True)
    sukunimi = models.CharField(max_length=64)
    yritys = models.CharField(max_length=64, blank=True)
    whatsapp = models.CharField(max_length=64, blank=True)
    hankejonkayhteys = models.ManyToManyField(Hanke)

    def __str__(self):
        return self.sukunimi

    class Meta:
        ordering = ('sukunimi',)


class Etu(models.Model):
    nimi = models.CharField(max_length=64)
    rank = models.IntegerField(default=1)
    tyyppi = models.CharField(max_length=64, blank=True)
    arvo = models.IntegerField(blank=True)
    kuva = models.ImageField(blank=True)
    hankejostasaatu = models.ForeignKey(Hanke, on_delete=models.CASCADE)

    def __str__(self):
        return self.nimi

    class Meta:
        ordering = ('-arvo',)


class Sijainti(models.Model):
    """Tämä taulu täyttyy pelkän postinumeron lisäämisellä (current US Postalcodes)."""
    posti_numero = models.CharField(max_length=5)
    paikka = models.CharField(blank=True, max_length=128)
    osavaltio = models.CharField(blank=True, max_length=128)
    lat = models.DecimalField(blank=True, max_digits=9, decimal_places=6)
    lon = models.DecimalField(blank=True, max_digits=9, decimal_places=6)

    def __str__(self):
        return str(self.posti_numero)

    def save(self, *args, **kwargs):
        kysely = requests.get(f'https://public.opendatasoft.com/api/records/1.0/search/?dataset=us-zip-code-latitude'
                              f'-and-longitude&q={self.posti_numero}&facet=state&facet=timezone&facet=dst')
        self.paikka = kysely.json()['records'][0]['fields']['city']
        self.osavaltio = kysely.json()['records'][0]['fields']['state']
        self.lat = kysely.json()['records'][0]['fields']['latitude']
        self.lon = kysely.json()['records'][0]['fields']['longitude']
        super().save(*args, **kwargs)




