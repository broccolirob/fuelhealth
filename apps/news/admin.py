from django.contrib import admin
from apps.news.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass