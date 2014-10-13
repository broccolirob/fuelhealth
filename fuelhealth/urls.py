from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from fuelhealth import settings

urlpatterns = patterns('',
    url(r'^$', 'apps.news.views.index', name='index'),
    url(r'^vote/$', 'apps.news.views.vote', name='vote'),
    url(r'^new/', 'apps.news.views.new', name='new'),
    url(r'^articles/$', 'apps.news.views.user_articles', name='user_articles'),
    url(r'^article/(?P<article_id>\w+)/$', 'apps.news.views.article_detail', name='article_detail'),
    url(r'^article/(?P<article_id>\w+)/delete/$', 'apps.news.views.delete_article', name='delete_article'),
    url(r'^comments/$', 'apps.news.views.user_comments', name='user_comments'),
    url(r'^comment/(?P<comment_id>\w+)/delete/$', 'apps.news.views.delete_comment', name='delete_comment'),
    url(r'^settings/(?P<user_id>\w+)/$', 'apps.accounts.views.settings', name='settings'),
    url(r'^rankings/$', 'apps.accounts.views.rankings', name='rankings'),
    url(r'^messages/', include('django_messages.urls')),
    url(r'^search/', include('haystack.urls')),

    url(r'data/$', 'apps.news.views.data', name='data'),
    url(r'^signin/$', 'apps.accounts.views.signin', name='signin'),

    url(r'^register/$', 'apps.news.views.register', name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
