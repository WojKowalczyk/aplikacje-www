from polls.models import Osoba, Stanowisko
from polls.serializers import OsobaModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# drf_serializer_test.md

stanowisko_och = Stanowisko(nazwa="Ochrona",opis="Ochrona")
osoba = Osoba(imie="Adam", nazwisko="Kowalski", plec="2", stanowisko = stanowisko_och)
stanowisko_och.save()
osoba.save()
serializer = OsobaModelSerializer(osoba)
serializer.data

{'imie': 'Adam', 'nazwisko': 'Kowalski', 'plec': 1, 'stanowisko': 4, 'data_dodania': '2024-11-07'}

content = JSONRenderer().render(serializer.data)
content

b'{"imie":"Adam","nazwisko":"Kowalski","plec":1,"stanowisko":4,"data_dodania":"2024-11-07"}'

import io
stream = io.BytesIO(content)
data = JSONParser().parse(stream)
deserializer = OsobaModelSerializer(data=data)
deserializer.is_valid()

True

deserializer.errors

{}

deserializer.fields

{'imie': CharField(max_length=200), 'nazwisko': CharField(max_length=200), 'plec': ChoiceField(choices=[(1, 'Kobieta'), (2, 'Mezczyzna')], required=False), 'stanowisko': PrimaryKeyRelatedField(queryset=Stanowisko.objects.all()), 'data_dodania': DateField(read_only=True)}

deserializer.validated_data

{'imie': 'Adam', 'nazwisko': 'Kowalski', 'plec': 1, 'stanowisko': <Stanowisko: Ochrona>}

deserializer.save()
deserializer.data

{'imie': 'Adam', 'nazwisko': 'Kowalski', 'plec': 1, 'stanowisko': 4}
