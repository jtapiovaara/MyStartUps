from django.db import models

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


class Etu(models.Model):
    nimi = models.CharField(max_length=64)
    tyyppi = models.CharField(max_length=64, blank=True)
    arvo = models.CharField(max_length=64, blank=True)
    kuva = models.ImageField(blank=True)
    hankejostasaatu = models.ForeignKey(Hanke, on_delete=models.CASCADE)

    def __str__(self):
        return self.nimi
