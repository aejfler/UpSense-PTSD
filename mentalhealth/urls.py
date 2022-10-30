"""mentalhealth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from sense.views import (ArticleDeleteView, ArticleDetailView,
                         ArticlesListView, BreathingDetailView, BreathingView,
                         ChecklistView, ContactDeleteView, CreateArticleView,
                         CreateEmergencyContact, CreateNotepadView,
                         CreateNoteView, CreatePodcastView,
                         CreateSafetyPlanView, DailyChecklistDetailView,
                         DailyChecklistEditView, DailyChecklistListView,
                         DashboardView, DeleteSafetyPlanView, DeleteUserView,
                         EditSafetyPlanView, EmergencyContactListView,
                         ErrorView, GetSupport, GoalsView, HomeView, LoginView,
                         LogoutView, ManageSymptomsView, MeditationDetailView,
                         MeditationsView, NoteDeleteView, NoteDetailView,
                         NoteEditView, NotepadDeleteView, NotepadDetailView,
                         NotepadEditView, NotepadListView, NotesListView,
                         PerspectiveView, PodcastDeleteView, PodcastDetailView,
                         PodcastListView, RegisterUserView, ResetPasswordView,
                         RIDExercisesView, SafetyPlanDetailView,
                         SafetyPlanView, TrackProgressView, TRExercisesView,
                         UserProfileView, ChecklistDeleteView)
from community.views import CreatePostView, EditPostView, DeletePostView, CommunityView, PostDetailView, \
    EditCommentView, DeleteCommentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', HomeView.as_view(), name='home'),
    path('', HomeView.as_view()),

    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('oauth/login/facebook/', include('social_django.urls', namespace='social')),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('reset_password/<int:pk>/', ResetPasswordView.as_view(), name='reset_password'),
    path('delete_account/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),

    path('notes/', NotesListView.as_view(), name='notes'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note_details'),
    path('new_note/', CreateNoteView.as_view(), name='create_note'),
    path('edit_note/<int:pk>/', NoteEditView.as_view(), name='edit_note'),
    path('delete_note/<int:pk>/', NoteDeleteView.as_view(), name='delete_note'),

    path('notepads/', NotepadListView.as_view(), name='notepads'),
    path('notepads/<int:pk>/', NotepadDetailView.as_view(), name='notepad_details'),
    path('new_notepad/', CreateNotepadView.as_view(), name='create_notepad'),
    path('edit_notepad/<int:pk>/', NotepadEditView.as_view(), name='edit_notepad'),
    path('delete_notepad/<int:pk>/', NotepadDeleteView.as_view(), name='delete_notepad'),

    path('daily_checklist/', ChecklistView.as_view(), name='checklist'),
    path('checklist_detail/<int:pk>/', DailyChecklistDetailView.as_view(), name='checklist_detail'),
    path('edit_checklist/<int:pk>/', DailyChecklistEditView.as_view(), name='edit_checklist'),
    path('checklists/', DailyChecklistListView.as_view(), name='checklists'),
    path('delete_checklist/<int:pk>/', ChecklistDeleteView.as_view(), name='delete_checklist'),

    path('podcasts/', PodcastListView.as_view(), name='podcasts'),
    path('podcast_detail/<int:pk>/', PodcastDetailView.as_view(), name='podcast_detail'),
    path('create_podcast/', CreatePodcastView.as_view(), name='create_podcast'),
    path('delete_podcast/<int:pk>/', PodcastDeleteView.as_view(), name='delete_podcast'),

    path('articles/', ArticlesListView.as_view(), name='articles'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_details'),
    path('create_article/', CreateArticleView.as_view(), name='create_article'),
    path('delete_article/<int:pk>/', ArticleDeleteView.as_view(), name='delete_article'),

    path('manage/', ManageSymptomsView.as_view(), name='manage_symptoms'),
    path('perspective/', PerspectiveView.as_view(), name='perspective'),
    path('meditations/', MeditationsView.as_view(), name='meditations'),
    path('meditation/<int:pk>/', MeditationDetailView.as_view(), name='meditation_detail'),
    path('breathings/', BreathingView.as_view(), name='breathings'),
    path('breathing/<int:pk>/', BreathingDetailView.as_view(), name='breathing_detail'),
    path('TRE/', TRExercisesView.as_view(), name='TREexercises'),
    path('RID/', RIDExercisesView.as_view(), name='RIDExercises'),

    path('add_contact/', CreateEmergencyContact.as_view(), name='create_emergency_contact'),
    path('contacts/', EmergencyContactListView.as_view(), name='contacts'),
    path('delete_contact/<int:pk>/', ContactDeleteView.as_view(), name='delete_contact'),

    path('progress/', TrackProgressView.as_view(), name='progress'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('goals/', GoalsView.as_view(), name='goals'),

    path('support/', GetSupport.as_view(), name='support'),



    path('create_safety_plan/', CreateSafetyPlanView.as_view(), name='create_safety_plan'),
    path('safety_plan/', SafetyPlanView.as_view(), name='safety_plan'),
    path('safety_plan_details/<int:pk>/', SafetyPlanDetailView.as_view(), name='safety_plan_details'),
    path('edit_safety_plan/<int:pk>/', EditSafetyPlanView.as_view(), name='edit_safety_plan'),
    path('delete_safety_plan/<int:pk>/', DeleteSafetyPlanView.as_view(), name='delete_safety_plan'),

    # COMMUNITY
    path('community/', CommunityView.as_view(), name='community'),

    path('post/create/', CreatePostView.as_view(), name='create_post'),
    path('post/edit/<slug:slug>/', EditPostView.as_view(), name='edit_post'),
    path('post/delete/<slug:slug>/', DeletePostView.as_view(), name='delete_post'),
    path('post_details/<slug:slug>/', PostDetailView.as_view(), name='post_details'),
    path('comment/edit/<int:pk>/', EditCommentView.as_view(), name='edit_comment'),
    path('comment/delete/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = ErrorView.as_view()
handler403 = ErrorView.as_view()
