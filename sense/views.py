from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from django.contrib.auth.models import Group
from sense.forms import (CreateArticleForm, CreateEmergencyContactForm,
                         CreateNoteForm, CreateNotepadForm, CreatePodcastForm,
                         CreateSafetyPlanForm, CreateUserForm,
                         DailyChecklistForm, EditChecklistForm, EditNoteForm,
                         EditNotepadForm, EditSafetyPlanForm, GoalsForm,
                         LoginUserForm, ResetPasswordForm, UserProfileForm)
from sense.models import (Article, Breathing, DailyChecklist, Goal, Meditation,
                          Note, NotePad, Person, Podcast, SafetyPlan)

User = get_user_model()


class ErrorView(View):
    def get(self, request, exception):
        return render(request, 'sense/errorTemplate.html')


class HomeView(ListView):
    template_name = 'sense/index.html'
    model = Article
    context_object_name = 'articles'


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'sense/user_profile.html'
    model = User
    success_url = reverse_lazy('dashboard')
    form_class = UserProfileForm


class LoginView(FormView):
    template_name = 'sense/login.html'
    success_url = reverse_lazy('dashboard')
    form_class = LoginUserForm

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class RegisterUserView(CreateView):
    template_name = 'sense/create_user.html'
    success_url = reverse_lazy('login')
    model = User
    form_class = CreateUserForm

    def form_valid(self, form):
        user_group = Group.objects.get(name='UpSenseUsers')
        cd = form.cleaned_data
        response = super().form_valid(form)
        self.object.set_password(cd['password'])
        self.object.groups.add(user_group)
        self.object.save()
        return response


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('home')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ResetPasswordView(LoginRequiredMixin, View):
    template_name = 'sense/reset_password.html'

    def get(self, request, *args, **kwargs):
        form = ResetPasswordForm()
        return render(request, self.template_name, {'form': form})


class CreateNoteView(LoginRequiredMixin, FormView):
    template_name = 'sense/create_note.html'
    model = Note
    form_class = CreateNoteForm
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        cd = form.cleaned_data
        Note.objects.create(title=cd['title'], note_content=cd['note_content'], notepad=cd['notepad'], user=self.request.user)
        return super().form_valid(form)


class NoteDetailView(LoginRequiredMixin, DetailView):
    template_name = 'sense/note_detail.html'
    model = Note
    context_object_name = 'note'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class NoteEditView(LoginRequiredMixin, UpdateView):
    template_name = 'sense/edit_note.html'
    model = Note
    form_class = EditNoteForm
    success_url = reverse_lazy('notes')


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('notes')


class NotesListView(LoginRequiredMixin, ListView):
    template_name = 'sense/list_of_notes.html'
    model = Note
    context_object_name = 'notes'
    ordering = 'date'

    def get_queryset(self):
        queryset = super(NotesListView, self).get_queryset().filter(user=self.request.user)
        return queryset


class CreateNotepadView(LoginRequiredMixin, FormView):
    template_name = 'sense/create_notepad.html'
    success_url = reverse_lazy('notes')
    model = NotePad
    form_class = CreateNotepadForm

    def form_valid(self, form):
        cd = form.cleaned_data
        NotePad.objects.create(notepad_name=cd['notepad_name'], user=self.request.user)
        return super().form_valid(form)


class NotepadListView(LoginRequiredMixin, ListView):
    template_name = 'sense/list_of_notepads.html'
    model = NotePad
    context_object_name = 'notepad'
    ordering = 'notepad_name'

    def get_queryset(self):
        queryset = super(NotepadListView, self).get_queryset().filter(user=self.request.user)
        return queryset


class NotepadDetailView(LoginRequiredMixin, DetailView):
    template_name = 'sense/notepad_detail.html'
    model = NotePad
    context_object_name = 'notepad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(notepad=self.kwargs.get('pk'))
        return context


class NotepadEditView(LoginRequiredMixin, UpdateView):
    template_name = 'sense/edit_notepad.html'
    model = NotePad
    form_class = EditNotepadForm
    success_url = reverse_lazy('notepads')


class NotepadDeleteView(LoginRequiredMixin, DeleteView):
    model = NotePad
    success_url = reverse_lazy('notepads')


class ChecklistView(LoginRequiredMixin, FormView):
    template_name = 'sense/checklist.html'
    success_url = reverse_lazy('progress')
    model = DailyChecklist
    form_class = DailyChecklistForm

    def form_valid(self, form):
        mood = form.cleaned_data["mood"]
        symptoms = form.cleaned_data["symptoms"]
        symptoms_intensity = form.cleaned_data["symptoms_intensity"]
        triggers = form.cleaned_data["triggers"]
        achievements = form.cleaned_data["achievements"]
        DailyChecklist.objects.create(mood=mood, symptoms=symptoms, symptoms_intensity=symptoms_intensity,
                                      triggers=triggers, achievements=achievements, user=self.request.user)
        return super().form_valid(form)


class DailyChecklistDetailView(LoginRequiredMixin, DetailView):
    template_name = 'sense/checklist_details.html'
    model = DailyChecklist
    context_object_name = 'checklist'

    def get_queryset(self):
        queryset = super(DailyChecklistDetailView, self).get_queryset().filter(user=self.request.user)
        return queryset


class DailyChecklistEditView(LoginRequiredMixin, UpdateView):
    template_name = 'sense/edit_checklist.html'
    model = DailyChecklist
    form_class = EditChecklistForm
    success_url = reverse_lazy('checklists')


class DailyChecklistListView(LoginRequiredMixin, ListView):
    template_name = 'sense/checklists.html'
    model = DailyChecklist
    context_object_name = 'checklists'
    ordering = '-date'

    def get_queryset(self):
        queryset = super(DailyChecklistListView, self).get_queryset().filter(user=self.request.user)
        return queryset


class ChecklistDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyChecklist
    success_url = reverse_lazy('checklists')


class GoalsView(LoginRequiredMixin, FormView):
    template_name = 'sense/goals.html'
    success_url = reverse_lazy('progress')
    model = Goal
    form_class = GoalsForm

    def form_valid(self, form):
        goal = form.cleaned_data["goal"]
        if goal == "1":
            target = 5
        elif goal == "2":
            target = 3
        elif goal == "3":
            target = 1
        elif goal == "4":
            target = 1

        Goal.objects.create(goal=goal, goal_target=target, user=self.request.user)
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, View):
    template_name = 'sense/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class TrackProgressView(LoginRequiredMixin, TemplateView):
    template_name = 'sense/track_progress.html'

    def get(self, request, *args, **kwargs):
        track = DailyChecklist.objects.all().order_by('date').filter(user=self.request.user)
        goals = Goal.objects.order_by("pk").filter(user=self.request.user)
        days = 0
        days_without_symptoms = DailyChecklist.objects.filter(symptoms_intensity__lte=0).order_by("date")\
            .filter(user=self.request.user)
        for i in range(len(days_without_symptoms) + 1):
            try:
                delta = days_without_symptoms[i + 1].date - days_without_symptoms[i].date
                if delta.days >= 1:
                    days += 1
            except IndexError:
                break

        return render(request, self.template_name, {"track": track, "goals": goals, "days_without_symptoms": days_without_symptoms,
                                                    "days": days})


class PodcastListView(ListView):
    template_name = 'sense/podcasts.html'
    model = Podcast
    context_object_name = 'podcasts'
    ordering = 'podcast_name'


class CreatePodcastView(PermissionRequiredMixin, CreateView):
    template_name = 'sense/create_podcast.html'
    model = Podcast
    form_class = CreatePodcastForm
    success_url = reverse_lazy('podcasts')
    permission_required = 'auth.add_podcast'

    def form_valid(self, form):
        cd = form.cleaned_data
        Podcast.objects.create(podcast_name=cd['podcast_name'], podcast=cd['podcast'])
        return super().form_valid(form)


class PodcastDetailView(DetailView):
    template_name = 'sense/podcast_detail.html'
    model = Podcast
    context_object_name = 'podcast'


class PodcastDeleteView(PermissionRequiredMixin, DeleteView):
    model = Podcast
    success_url = reverse_lazy('podcasts')
    permission_required = "sense.delete_podcast"


class CreateArticleView(PermissionRequiredMixin, CreateView):
    template_name = 'sense/create_article.html'
    model = Article
    form_class = CreateArticleForm
    success_url = reverse_lazy('articles')
    permission_required = "sense.add_article"

    def form_valid(self, form):
        cd = form.cleaned_data
        Article.objects.create(title=cd['title'], slug=cd['slug'], author=cd['author'], content=cd['content'],
                               status=cd['status'])
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    template_name = 'sense/article_details.html'
    model = Article
    context_object_name = 'article'


class ArticlesListView(ListView):
    template_name = 'sense/articles.html'
    model = Article
    context_object_name = 'articles'


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('articles')
    permission_required = "sense.delete_article"


class ManageSymptomsView(LoginRequiredMixin, ListView):
    template_name = 'sense/management_tools.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class PerspectiveView(LoginRequiredMixin, View):
    template_name = 'sense/perspective.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class BreathingView(LoginRequiredMixin, ListView):
    template_name = 'sense/breathings.html'
    model = Breathing
    context_object_name = 'breathings'
    ordering = 'uploaded_date'


class BreathingDetailView(LoginRequiredMixin, DetailView):
    template_name = 'sense/breathing_details.html'
    model = Breathing
    context_object_name = 'breathing'


class MeditationsView(LoginRequiredMixin, ListView):
    template_name = 'sense/meditations.html'
    model = Meditation
    context_object_name = 'meditations'
    ordering = 'title'


class MeditationDetailView(LoginRequiredMixin, DetailView):
    template_name = 'sense/meditation_detail.html'
    model = Meditation
    context_object_name = 'meditation'


class TRExercisesView(LoginRequiredMixin, View):
    template_name = 'sense/TREexercises.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RIDExercisesView(LoginRequiredMixin, View):
    template_name = 'sense/RIDExercises.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CreateEmergencyContact(LoginRequiredMixin, FormView):
    template_name = 'sense/create_person.html'
    success_url = reverse_lazy('contacts')
    model = Person
    form_class = CreateEmergencyContactForm

    def form_valid(self, form):
        cd = form.cleaned_data
        Person.objects.create(name=cd['name'], phone=cd['phone'], user=self.request.user)
        return super().form_valid(form)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Person
    success_url = reverse_lazy('contacts')


class EmergencyContactListView(LoginRequiredMixin, ListView):
    template_name = 'sense/contact_list.html'
    model = Person
    context_object_name = 'contacts'
    ordering = 'name'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class CreateSafetyPlanView(LoginRequiredMixin, FormView):
    template_name = 'sense/create_safety_plan.html'
    success_url = reverse_lazy('safety_plan')
    model = SafetyPlan
    form_class = CreateSafetyPlanForm

    def form_valid(self, form):
        cd = form.cleaned_data
        SafetyPlan.objects.create(warning_signs=cd['warning_signs'], coping_strategies=cd['coping_strategies'],
                                  emergency_contacts=cd['emergency_contacts'], safe_places=cd['safe_places'],
                                  professional_help=cd['professional_help'],
                                  environmental_safety=cd['environmental_safety'],
                                  other_suggestions=cd['other_suggestions'], user=self.request.user)
        return super().form_valid(form)


class SafetyPlanView(LoginRequiredMixin, ListView):
    template_name = 'sense/list_of_safetyplan.html'
    model = SafetyPlan
    context_object_name = 'plans'
    ordering = 'name'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class SafetyPlanDetailView(LoginRequiredMixin, DetailView):
    template_name = 'sense/safety_plan_details.html'
    model = SafetyPlan
    context_object_name = 'plan'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class EditSafetyPlanView(LoginRequiredMixin, UpdateView):
    template_name = 'sense/edit_safety_plan.html'
    model = SafetyPlan
    form_class = EditSafetyPlanForm
    success_url = reverse_lazy('safety_plan')


class DeleteSafetyPlanView(LoginRequiredMixin, DeleteView):
    model = SafetyPlan
    success_url = 'home'


class GetSupport(LoginRequiredMixin, View):
    template_name = 'sense/support.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

