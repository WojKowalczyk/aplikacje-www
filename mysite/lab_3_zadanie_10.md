import django
django.setup()
from polls.models import Osoba, Stanowisko
osoby = Osoba.objects.all()
osoby_id3 = Osoba.objects.filter(id=3)
osoby_imie_odlitery = Osoba.objects.filter(imie__startswith="J")
alfabetycznie_stanowiska = Stanowisko.objects.order_by("nazwa")
nowy_stanowisko = Stanowisko(nazwa="Manager",opis="Manager")
nowy = Osoba(imie="Marek",nazwisko="Ząb",plec=2, stanowisko=nowy_stanowisko)
nowy_stanowisko.save()
nowy.save()