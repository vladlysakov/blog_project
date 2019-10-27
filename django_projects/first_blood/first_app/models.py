from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.signals import user_logged_in, user_logged_out


class Article(models.Model):
    author = models.ForeignKey('User_Profile', on_delete=models.SET_NULL, null=True)
    title  = models.CharField(max_length=30, verbose_name='title')
    topic = models.CharField(max_length=20, verbose_name='topic')
    content = models.TextField(verbose_name='content')
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name='creation date')
   

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def get_absolute_url(self):
        return '/blog/user/{}'.format(self.title)

    
class User_Profile(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, verbose_name='Age')
    logout_time = models.DateTimeField(null=True, verbose_name='Last logout')
    time_last_logout = models.DurationField(null=True)
    

    class Meta:
        verbose_name_plural = 'Persons'
        verbose_name = 'Person'


    @receiver(user_logged_out)  #Both methods(@receiver) calculate last login time 
    def get_time(sender, user, request, **kwargs):
        try:
            sender.objects.filter(pk=user.pk).update(logout_time=now())
        except sender.DoesNotExist:
            return None

    @receiver(user_logged_in)
    def get_session_time(sender, user, request, **kwargs):
        try:
            print(request.user.last_login)
            diff_time = now() - user.logout_time
            sender.objects.filter(pk=user.pk).update(time_last_logout=diff_time)
        except (sender.DoesNotExist, TypeError):
            return None
