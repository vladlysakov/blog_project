from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User_Profile, Article


class UserForm(UserCreationForm):
    class Meta:
        model = User_Profile
        fields  = ('username', 'age')

        
class AddArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'topic', 'content')


class UpdateInfoForm(ModelForm):
    class Meta:
        model = User_Profile
        fields = ('username', 'first_name',
                  'last_name', 'email',
                  'password', 'age')
