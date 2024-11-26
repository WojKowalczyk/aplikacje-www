from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import datetime
from django.utils import timezone
from django.db import models
from django.contrib import admin
from django.utils.html import format_html

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Stanowisko(models.Model):
    nazwa = models.CharField(max_length = 200, blank = False)
    opis = models.CharField(max_length = 200)

    def __str__(self):
        return str(self.nazwa)

    # nazwa - pole tekstowe, wymagane, niepuste
    # opis - pole tekstowe, opcjonalne
class Osoba(models.Model):
    imie = models.CharField(max_length = 200, blank = False)
    nazwisko = models.CharField(max_length = 200, blank = False)
    class Plcie(models.IntegerChoices):
        Kobieta = 1
        Mezczyzna = 2
    plec = models.IntegerField(choices=Plcie.choices, default=1)
    stanowisko = models.ForeignKey(Stanowisko, on_delete=models.CASCADE)
    data_dodania = models.DateField(auto_now_add=True)
    wlasciciel = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    @admin.display
    def id_stanowisko(self):
        return (str(self.stanowisko.nazwa) + str(self.stanowisko.id))


    class Meta:
        ordering = ["nazwisko"]
        permissions = [
            ("can_view_other_persons", "Can view other persons"),  # Custom permission
        ]
    def __str__(self):
        return str(self.imie + " " + self.nazwisko)
    # imie - pole tekstowe, wymagane, niepuste (sprawdź dokumentację z pkt. 2)
    # nazwisko - pole tekstowe, wymagane, niepuste
    # plec - pole wyboru (kobieta, mężczyzna, inne)
    # stanowisko - klucz obcy do modelu Stanowisko (do utworzenia w kolejnym kroku).


