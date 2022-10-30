from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import (LoginRequiredMixin)
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from .models import Post, Comment
from taggit.models import Tag
from .forms import CreatePostForm, EditPostForm, CommentForm, EditCommentForm, SearchForm

User = get_user_model()


class CommunityView(LoginRequiredMixin, ListView):
    template_name = 'community/community_home.html'
    context_object_name = 'comments'

    def get(self, request, *args, **kwargs):
        form = SearchForm()
        posts = Post.objects.order_by('-created').prefetch_related('tags').all()
        paginator = Paginator(posts, 8)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'posts': posts, 'page': page, 'form': form})

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        if form.is_valid():
            tagged = form.cleaned_data['search']
            tagged_posts = Post.objects.filter(Q(tags__name__icontains=form.cleaned_data['search']) |
                                               Q(title__icontains=form.cleaned_data['search'])).distinct()
            return render(request, self.template_name, {'tagged': tagged, 'tagged_posts': tagged_posts, 'form': form})
        return render(request, self.template_name, {'form': form})


class CreatePostView(LoginRequiredMixin, FormView):
    template_name = 'community/create_post.html'
    model = Post
    form_class = CreatePostForm
    success_url = reverse_lazy('community')

    def form_valid(self, form):
        cd = form.cleaned_data
        new_post = Post.objects.create(title=cd['title'], category=cd['category'], content=cd['content'], author=self.request.user)
        tagged = cd['tags']
        for t in tagged:
            new_post.tags.add(t)
        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, UpdateView):
    template_name = 'community/edit_post.html'
    model = Post
    form_class = EditPostForm
    success_url = reverse_lazy('community')

    def get_queryset(self):
        queryset = super(EditPostView, self).get_queryset().filter(author=self.request.user)
        return queryset


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('community')


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'community/post_details.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm
        context['comments'] = Comment.objects.filter(post__slug=self.kwargs.get('slug'))
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        author = request.user
        form = CommentForm(data=request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = author
            new_comment.save()
        else:
            form = CommentForm()

        return redirect('post_details', post.slug)


class EditCommentView(UpdateView):
    template_name = 'community/edit_comment.html'
    model = Comment
    form_class = EditCommentForm


class DeleteCommentView(DeleteView):
    model = Comment
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        post = self.object.post
        return reverse_lazy("post_details", kwargs={'slug': post.slug})
