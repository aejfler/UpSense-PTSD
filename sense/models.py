from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .validators import validate_intensity


class NotePad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notepad_name = models.CharField(max_length=50)

    def __str__(self):
        return self.notepad_name


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, editable=True)
    notepad = models.ForeignKey(NotePad, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    note_content = models.TextField()

    def __str__(self):
        return self.title


MOOD = [
    ('J', 'Feeling Joy'),
    ('M', 'Motivated'),
    ('P', 'Staying Positive'),
    ('I', 'Improving'),
    ('S', 'Sad'),
    ('A', 'Anxious'),
    ('H', 'Hopeless'),
    ('V', 'Avoiding Triggers'),
    ('R', 'Angry'),
    ('D', 'Distracted'),
    ('L', 'Lost'),
    ('F', 'Afraid'),
    ('ST', 'Struggling'),
]


class DailyChecklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood = models.CharField(max_length=2, choices=MOOD, default='')
    symptoms = models.TextField(help_text='Describe what symptoms have you experienced today?')
    symptoms_intensity = models.IntegerField(validators=[validate_intensity], blank=True, null=True)
    triggers = models.TextField(help_text='What triggers have you experienced today?')
    achievements = models.TextField(help_text='What have you accomplished today?')

    def __str__(self):
        return 'Daily checklist from: ' + str(self.date)


GOALS = [
    ("1", 'Symptoms intensity below 5'),
    ("2", 'Symptoms intensity below 3'),
    ("3", 'Symptoms intensity below 2'),
    ("4", 'Symptoms intensity below 1'),
]


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(choices=GOALS, max_length=2000, blank=True)
    goal_target = models.IntegerField(default=0)

    def __str__(self):
        return self.goal


class Podcast(models.Model):
    uploaded_date = models.DateField(auto_now_add=True)
    podcast_name = models.CharField(max_length=128)
    author = models.CharField(max_length=128, default="UpSense Team")
    podcast = models.FileField(verbose_name="Podcast")

    def __str__(self):
        return self.podcast_name


class Meditation(models.Model):
    uploaded_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128, default="UpSense Team")
    meditation_file = models.FileField(verbose_name="Meditation")

    def __str__(self):
        return self.title


class Breathing(models.Model):
    uploaded_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128, default="UpSense Team")
    breathing_file = models.FileField(verbose_name="Breathing exercise")

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')
    content = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


STRATEGIES = [
    ('1', 'Physical exercises'),
    ('2', 'Prayer or engaging in other spiritual activity'),
    ('3', 'Count slowly to 100 and backwards'),
    ('4', 'Phone call to mentor or friend'),
    ('5', 'Meet with someone'),
    ('6', 'Go for a walk outside'),
    ('7', 'Focus on breathing'),
    ('8', 'Play with or hug a pet'),
    ('9', 'Let shed tears'),
    ('10', 'other...'),

]


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Name')
    phone = models.CharField(max_length=10, verbose_name='Phone')
    address = models.CharField(max_length=128, verbose_name='Address', blank=True, default='None')

    def __str__(self):
        return self.name


class SafetyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='Safety Plan name', default='SafetyPlan1')

    warning_signs = models.TextField(max_length=3000, verbose_name='Warning signs', help_text='Warning signs can be '
                                                                                              'thoughts, feelings or '
                                                                                              'behaviours that appear '
                                                                                              'or increase when you '
                                                                                              'get distressed.')
    coping_strategies = models.CharField(choices=STRATEGIES, max_length=50, verbose_name='Coping Strategies')
    emergency_contacts = models.ForeignKey(Person, on_delete=models.CASCADE, default='',
                                           help_text='Consider who you could contact with to take your '
                                                     'mind off your thoughts or who could help you feel '
                                                     'better')
    safe_places = models.CharField(max_length=1024, help_text='Think of any places where you could go to feel safe or '
                                                              'where you could seek comfort when you find yourself in'
                                                              ' crisis.')

    professional_help = models.CharField(max_length=1024, help_text='What medical or mental health professionals can '
                                                                    'you contact in time of crisis? You can also '
                                                                    'include your therapist information here.')

    environmental_safety = models.CharField(max_length=1200, help_text='Think of any objects in your environmental '
                                                                       'that could pose a risk to your safety. That '
                                                                       'could be weapons, drugs, alcohol, toxins or '
                                                                       'anything you could use to self-harm.')
    other_suggestions = models.CharField(max_length=2000, help_text='If you think of anything that '
                                                                    'could help you in time of crisis'
                                                                    ' attach them here.', blank=True)



