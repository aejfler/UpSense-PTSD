from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.core.exceptions import ValidationError

from sense.models import (STRATEGIES, Article, DailyChecklist, Goal, Note,
                          NotePad, Person, Podcast, SafetyPlan)

User = get_user_model()


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError('Enter a correct data!')


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {
            "username": ''
        }

    def clean(self):
        cd = super().clean()
        repeat_password = cd.get('repeat_password')
        password = cd.get('password')
        validate_password(password)
        if password != repeat_password:
            raise ValidationError('Password must be the same!')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    repeat_new_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        new_password = cd.get('new_password')
        repeat_new_password = cd.get('repeat_new_password')
        validate_password(new_password)
        if new_password != repeat_new_password:
            raise ValidationError('Password must be the same!')


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'note_content', 'notepad']

        widgets = {
            'notepad': forms.Select()
        }


class CreateNotepadForm(forms.Form):
    notepad_name = forms.CharField(max_length=128)
    labels = {
        'notepad_name': 'Notepad:'
    }


class EditNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'note_content', 'notepad']


class DeleteNoteView(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'note_content', 'notepad']


class EditNotepadForm(forms.ModelForm):
    class Meta:
        model = NotePad
        fields = ['notepad_name']


class DeleteNotepadForm(forms.ModelForm):
    class Meta:
        model = NotePad
        fields = ['notepad_name']


class DailyChecklistForm(forms.ModelForm):
    class Meta:
        model = DailyChecklist
        fields = ['mood', 'triggers', 'achievements', 'symptoms', 'symptoms_intensity']
        widgets = {
            'symptoms_intensity': forms.HiddenInput()
        }


class EditChecklistForm(forms.ModelForm):
    class Meta:
        model = DailyChecklist
        fields = ['mood', 'triggers', 'achievements', 'symptoms', 'symptoms_intensity']
        widgets = {
            'symptoms_intensity': forms.HiddenInput()
        }


class CreatePodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['podcast_name', 'podcast']


class DeletePodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = '__all__'


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'author', 'content', 'status']


class DeleteArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class CopingStrategiesForm(forms.Form):
    strategies = forms.MultipleChoiceField(choices=STRATEGIES, required=False)


class CreateEmergencyContactForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'phone']


class ContactDeleteForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class CreateSafetyPlanForm(forms.ModelForm):
    class Meta:
        model = SafetyPlan
        fields = ['name', 'warning_signs', 'coping_strategies', 'emergency_contacts', 'safe_places', 'professional_help',
                  'environmental_safety', 'other_suggestions']
        widgets = {
        }


class EditSafetyPlanForm(forms.ModelForm):

    class Meta:
        model = SafetyPlan
        fields = ['name', 'warning_signs', 'coping_strategies', 'emergency_contacts', 'safe_places', 'professional_help',
                  'environmental_safety', 'other_suggestions']


class DeleteSafetyPlanForm(forms.ModelForm):
    class Meta:
        model = SafetyPlan
        fields = '__all__'


class GoalsForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal']


class DeleteChecklistForm(forms.ModelForm):
    class Meta:
        model = DailyChecklist
        fields = '__all__'
