from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from apps.news.models import Article
from haystack.forms import SearchForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))


    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class ArticleForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digital Health Is on the Rise'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'www.medcitynews.com/digital-health-is-on-the-rise'}))

    class Meta:
        model = Article
        exclude = ('points', 'moderator', 'voters')


class ArticleSearchForm(SearchForm):

    q = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search articles'}))

    def no_query_found(self):
        return self.searchqueryset.all()