from django.contrib import admin

from sense.models import (Article, Breathing, DailyChecklist, Goal, Meditation,
                          Note, NotePad, Podcast)

admin.site.register(NotePad)
admin.site.register(Note)
admin.site.register(DailyChecklist)
admin.site.register(Goal)
admin.site.register(Podcast)
admin.site.register(Meditation)
admin.site.register(Breathing)
admin.site.register(Article)

