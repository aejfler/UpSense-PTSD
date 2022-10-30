import pytest
from django.contrib.auth.models import User
from factories import (UserFactory, ArticleFactory, BreathingFactory, GoalFactory,
                       MeditationFactory, NoteFactory, NotepadFactory, DailyChecklistFactory,
                       PersonFactory, PodcastFactory, SafetyPlanFactory)
from pytest_factoryboy import register

register(UserFactory)
register(NoteFactory)
register(DailyChecklistFactory)
register(NotepadFactory)
register(PersonFactory)
register(ArticleFactory)
register(GoalFactory)
register(MeditationFactory)
register(BreathingFactory)
register(PodcastFactory)
register(SafetyPlanFactory)

#by registering new factory the name from now on will be note_factory


@pytest.fixture()
def user():
    return {'username': 'user1', 'email': 'user1@gmail.com', 'first_name': 'userTest'}


@pytest.fixture()
def create_user(user):
    user_test_object = User.objects.create(**user)
    user_test_object.set_password('confident')
    return user_test_object


@pytest.fixture
def authenticated_user(db, client, user):
    test_user = User.objects.create_user(**user)
    test_user.set_password(user.get('password'))
    test_user.save()
    logged = client.login(**user)
    return test_user, logged

