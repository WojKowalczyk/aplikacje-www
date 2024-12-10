import graphene
from graphene_django import DjangoObjectType

from polls.models import Osoba, Stanowisko, Question, Choice


# dzięki wykorzystaniu klasy DjangoObjectType możemy w łatwy sposób
# wskazać klasę wcześniej zdefiniowanego modelu, która zostanie wykorzystana
# w schemie GraphQL umożliwiając połączenie Django QuerySet oraz zapytań
# poprzez GraphQL. Podobnie jak w przypadku definicji własności w klasach
# administracyjnych danego modelu (plik admin.py) tutaj też możemy określić
# np. listę pól, które poprzez GraphQL chcemy wystawić z danego modelu
class OsobaType(DjangoObjectType):
    class Meta:
        model = Osoba
        fields = ("id", "name", "shirt_size", "miesiac_dodania", "Stanowisko")
        # lub
        # fields = "__all__"

class StanowiskoType(DjangoObjectType):
    class Meta:
        model = Stanowisko
        fields = ("id", "name", "country")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("question_text", "pub_date")

class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = ("question", "choice_text", "votes")

# klasa Query pozwala określić pola (tu np. all_Stanowiskos, Osoba_by_id, itd.)
# które są dostępne, a następnie Resolvery, który definiują w jaki sposób
# dane dla wskazanego pola będą pobierane (tu już używamy znany nam
# sposób z użyciem Django QuerySet)

class Query(graphene.ObjectType):
    # typ graphene.List określa, że zwracana będzie lista obiektów danego typu
    all_Stanowiskos = graphene.List(StanowiskoType)

    # tu określamy, że zwrócony będzie obiekt typu OsobaType, a jego wyszukanie
    # odbędzie się na podstawie jego atrybutu id o typie Int, który jest wymagany
    Osoba_by_id = graphene.Field(OsobaType, id=graphene.Int(required=True))

    all_Osobas = graphene.List(OsobaType)
    Osoba_by_name = graphene.Field(OsobaType, name=graphene.String(required=True))
    find_Osobas_name_by_phrase = graphene.List(OsobaType, substr=graphene.String(required=True))
    all_Questions = graphene.List(QuestionType)
    all_Choices = graphene.List(ChoiceType)
    find_Question_first_letter = graphene.List(QuestionType, substr=graphene.String(required=True))

    # resolver dla pola all_Stanowiskos
    # root główny obiekt wartości przekazywany przez zapytanie
    # info informacje z resolvera
    # args słownik (opcjonalnie), parametrów przekazywanych do resolvera
    def resolve_all_Stanowiskos(root, info):
        return Stanowisko.objects.all()

    def resolve_Osoba_by_id(root, info, id):
        try:
            return Osoba.objects.get(pk=id)
        except Osoba.DoesNotExist:
            raise Exception('Invalid Osoba Id')

    def resolve_Osoba_by_name(root, info, name):
        try:
            return Osoba.objects.get(name=name)
        except Osoba.DoesNotExist:
            raise Exception(f'No Osoba with name \'{name}\' found.')

    def resolve_all_Osobas(root, info):
        """ zwraca również wszystkie powiązane obiekty Stanowisko dla tego obiektu Osoba"""
        return Osoba.objects.select_related("Stanowisko").all()

    def resolve_find_Osobas_name_by_phrase(self, info, substr):
        return Osoba.objects.filter(name__icontains=substr)

    def resolve_all_Questions(root,info):
        return Question.objects.all()

    def resolve_all_Choices(root, info):
        return Choice.objects.all()

    def resolve_Question_name_by_first_letter(root, info, substr):
        return Question.objects.filter(name__icontains=substr)



schema = graphene.Schema(query=Query)