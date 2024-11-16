from rest_framework import serializers
from .models import Osoba, Stanowisko, Choice, Question
from datetime import datetime

class QuestionSerializer(serializers.Serializer):
    #id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField("date published")
    def create(self, validated_data):
        return Question.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.question_text = validated_data.get("question_text",instance.question_text)
        instance.pub_date = validated_data.get("pub_date",instance.pub_date)
        instance.save()
        return instance


class ChoiceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["question","choice_text","votes"]


class OsobaModelSerializer(serializers.ModelSerializer):
    wlasciciel = serializers.ReadOnlyField(source='wlasciciel.username')
    class Meta:
        model = Osoba
        fields = ["imie","nazwisko","plec","stanowisko","data_dodania", "wlasciciel"]
    def validate_imie(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Powinny być same litery.")
        return value
    def validate_nazwisko(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Powinny być same litery.")
        return value
    def validate_data_dodania(self, value):
        if value > datetime.today():
            raise serializers.ValidationError("Data nie może być z przyszłości")
        return

    def update(self, instance, validated_data):
        instance.name = validated_data.get('imie', instance.imie)
        instance.shirt_size = validated_data.get('nazwisko', instance.nazwisko)
        instance.data_dodanie = validated_data.get('data_dodania', instance.data_dodania)
        instance.stanowisko = validated_data.get('stanowisko', instance.stanowisko)
        instance.plec = validated_data.get("plec",instance.plec)
        instance.wlasciciel = validated_data.get("wlasciciel",instance.wlasciciel)
        instance.save()
        return instance

class StanowiskoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanowisko
        fields = ["nazwa","opis"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('nazwa', instance.nazwa)
        instance.description = validated_data.get('opis', instance.opis)
        instance.save()
        return instance