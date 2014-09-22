from haystack import indexes
from django.utils import timezone
from apps.news.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    moderator = indexes.CharField(model_attr='moderator')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(created_at__lte=timezone.now())