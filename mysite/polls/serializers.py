from rest_framework import serializers
from .models import Osoba, Stanowisko, Choice, Question

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
    class Meta:
        model = Osoba
        fields = ["imie","nazwisko","plec","stanowisko","data_dodania"]

class StanowiskoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stanowisko
        fields = ["nazwa","opis"]