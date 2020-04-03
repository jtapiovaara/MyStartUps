# Generated by Django 3.0.4 on 2020-03-09 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hanke',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=32)),
                ('tyyppi', models.CharField(blank=True, max_length=32)),
                ('miksi', models.TextField(blank=True)),
                ('tavoite', models.TextField(blank=True, max_length=32)),
                ('aika', models.CharField(blank=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Yhteys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etunimi', models.CharField(blank=True, max_length=64)),
                ('sukunimi', models.CharField(max_length=64)),
                ('yritys', models.CharField(blank=True, max_length=64)),
                ('whatsapp', models.CharField(blank=True, max_length=64)),
                ('hankejonkayhteys', models.ManyToManyField(to='msu.Hanke')),
            ],
        ),
        migrations.CreateModel(
            name='Etu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nimi', models.CharField(max_length=64)),
                ('tyyppi', models.CharField(blank=True, max_length=64)),
                ('arvo', models.CharField(blank=True, max_length=64)),
                ('hankejostasaatu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msu.Hanke')),
            ],
        ),
    ]