import random
from taggit.managers import TaggableManager
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy


class Post(models.Model):
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name='title')
    content = models.TextField(help_text='Describe your question/thoughts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    category = models.CharField(max_length=35)
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse_lazy("post_details", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            rand = random.randint(100_000, 500_000)
            self.slug = slugify(f'{self.title}-{rand}')
        super().save(*args, **kwargs)
        return self.slug

    def __str__(self):
        return self.title


class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name='created')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='by')
    content = models.TextField(max_length=8000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def get_absolute_url(self):
        return reverse("post_details", kwargs={'slug': self.post.slug})

    def __str__(self):
        return self.content




