import factory
import factory.fuzzy
from faker import Faker
from django.contrib.auth.models import User
from sense.models import (Article, Breathing, DailyChecklist, Goal, Meditation,
                          Note, NotePad, Person, Podcast, SafetyPlan, STRATEGIES, MOOD)

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()


class NotepadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NotePad

    notepad_name = fake.name()


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    notepad = factory.SubFactory(NotepadFactory)
    note_content = fake.text()
    date = ''
    title = "Note1"  # to są default values


class DailyChecklistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DailyChecklist

    date = fake.date()
    mood = factory.fuzzy.FuzzyChoice(MOOD, getter=lambda c: c[0])
    symptoms = "dizziness"
    symptoms_intensity = 5
    triggers = "crowd of people"
    achievements = "none"


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal


class PodcastFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Podcast
    # podcast_name = ''
    # uploaded_date = ""
    # podcast = fake.


class MeditationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meditation


class BreathingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Breathing


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    name = fake.name()
    phone = fake.numerify()
    address = fake.address()


class SafetyPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SafetyPlan

    # class Params:
    #     """creating a Person instance which is discarded before calling a model. This able to provide a profile/instance
    #      to the factory """
    #     emergency = factory.SubFactory(PersonFactory)

    name = fake.word(),
    warning_signs = fake.sentences(1),
    coping_strategies = factory.fuzzy.FuzzyChoice(STRATEGIES, getter=lambda c: c[1])
    emergency_contacts = factory.SubFactory(PersonFactory)
    safe_places = fake.city(),
    professional_help = fake.name(),
    environmental_safety = fake.word(),
    other_suggestions = fake.word(),
