from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from apps.accounts.models import Profile
from apps.news.models import Article, Comment
from haystack.forms import SearchForm

# This form looks the same as the built in django one?
class AuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Please enter a correct username and password.")
        return self.cleaned_data


# Any of these auth related forms are probably better suited to be in a forms.py in your account app
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frist Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "username", "password1", "password2")


class ProfileForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "email", "username", "profile_pic")


class ArticleForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digital Health Is on the Rise'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'www.medcitynews.com/digital-health-is-on-the-rise'}))

    class Meta:
        model = Article
        exclude = ('points', 'moderator', 'voters', 'flags')


class ArticleSearchForm(SearchForm):

    q = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search articles'}))

    def no_query_found(self):
        return self.searchqueryset.all()


class CommentForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        exclude = ('article', 'author', 'points', 'voters', 'created_at', 'flags')
