from django.contrib import admin

from community.models import Post, Comment
# admin.site.register(Post)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'author', 'get_tags']

    def get_tags(self, obj):
        return ', '.join(t for t in obj.tags.names())


admin.site.register(Comment)
