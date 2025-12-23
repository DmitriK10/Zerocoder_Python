from django.contrib import admin
from .models import News_post

@admin.register(News_post)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('title', 'short_description', 'text')
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)