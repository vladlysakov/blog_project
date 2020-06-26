from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User_Profile, Article


class PinForm(forms.Form):
    pin = forms.CharField(max_length=10)


class UserForm(UserCreationForm):
    class Meta:
        model = User_Profile
        fields = ('username', 'age', 'phone')


class AddArticleForm(ModelForm):
    topic = forms.CharField(required=False)

    class Meta:
        model = Article
        fields = ('title', 'topic', 'content')


class UpdateInfoForm(ModelForm):
    class Meta:
        model = User_Profile
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'phone')
