# Generated by Django 5.1.2 on 2024-10-30 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_osoba_plec'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='osoba',
            options={'ordering': ['nazwisko']},
        ),
    ]
