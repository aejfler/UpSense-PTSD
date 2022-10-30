import pytest
from django import urls
from django.contrib.auth.models import User
from sense.models import DailyChecklist, Note, NotePad, Person, SafetyPlan


@pytest.mark.django_db
def test_create_user():
    """this test checks if new user is created and saved to the database"""
    count = User.objects.all().count()
    print(count)
    User.objects.create(username='user1', email='user1@gmail.com', first_name='userTest')
    print(User.objects.count())
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_add_user(client):
    """test checks if new user can be successfully register"""
    data = {
        "username": "AlexFly",
        "first_name": "Alex",
        "email": "alex1@gmail.com",
    }
    register = urls.reverse('login')
    response = client.post(register, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_set_user_password(user_factory):
    """setting user password using set_password method and verifying it with assistance of factory"""
    obj = user_factory.create()
    obj.set_password("passwordTEST")
    assert obj.check_password("passwordTEST") is True


@pytest.mark.django_db
def test_login_user(client, create_user, user):
    """test check login view with data provided by fixtures "user" and  "create_user" """
    user_model = User
    assert user_model.objects.count() == 1
    login_url = urls.reverse('login')
    resp = client.post(login_url, data=user)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_user_logout(client, authenticated_user):
    """testing user logout view with success url redirection"""
    logout_url = urls.reverse('logout')
    resp = client.get(logout_url, follow=True)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_create_note(note_factory):
    """this test checks creating new note and examine connection to foreign key, build dependencies with tables"""
    note = note_factory.create()
    assert note
    note.title = 'gen234' #here we can overrite default value declared in factory
    note.date = '1998-12-12' #here we can overrite default value declared in factory



@pytest.mark.django_db
def test_note_detail_view(client, note):
    response = client.get(f'/note/{note.pk}/')
    print(Note.objects.count())
    print(Note.objects.get(pk=note.pk))
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_notepad(notepad_factory):
    """adding to database notepad with name generated with faker"""
    notepad_factory.create()
    print(notepad_factory.notepad_name)
    assert True


@pytest.mark.django_db
def test_notepad_detail_view(client, note_pad):
    response = client.get(f'/note/{note_pad.pk}/')
    print(NotePad.objects.count())
    print(NotePad.objects.get(pk=note_pad.pk))
    assert response.status_code == 302



@pytest.mark.django_db
def test_create_person(client, person_factory, authenticated_user):
    """test checks creating emergency contact"""

    contact = person_factory.build()
    assert contact
    contact_url = urls.reverse('create_emergency_contact')
    response = client.post(contact_url, data=contact, content_type='multipart/form-data', follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_safety_plan_instance(safety_plan_factory, client, authenticated_user):
    """test checks creating a new safety plan and storing it in database"""
    plan = safety_plan_factory.create()
    assert plan
    plan_redirect = urls.reverse('create_safety_plan')
    response = client.post(plan_redirect, data=plan, content_type='multipart/form-data', follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_checklist(daily_checklist_factory, client, authenticated_user):
    """test checks creating a new daily checklists and storing it in database. Also verifies if user is logged in"""
    checklist = daily_checklist_factory.create()
    assert checklist
    checklist_redirect = urls.reverse('checklist')
    response = client.post(checklist_redirect, data=checklist, content_type='multipart/form-data', follow=True)
    assert response.status_code == 200


