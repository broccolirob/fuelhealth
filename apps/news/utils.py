import datetime
from django.utils.timezone import utc
from apps.news.models import Article

# This file could use some docuemntation love for your score algorithms
def calculate_score(votes, item_hour_age, gravity=1.8):
    return (votes - 1) / pow((item_hour_age + 2), gravity)


def score(article, gravity=1.8, timebase=120):
    points = (article.points - 1)**0.8
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    age = int((now - article.created_at).total_seconds())/60
    return points/(age+timebase)**1.8


def top_articles(top=180, consider=1000):
    latest_articles = Article.objects.order_by('-created_at')[:consider]
    # Instead of sorting on a list with the score, then making another list which dumps the score
    # you could just use http://stackoverflow.com/questions/3216398/sorting-by-arbitrary-lambda-in-python
    ranked_articles = sorted([(score(article), article) for article in latest_articles], reverse=True)
    return [article for _, article in ranked_articles][:top]
