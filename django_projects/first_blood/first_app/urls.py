"""first_blood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.template.response import TemplateResponse
from axes import decorators
from .views import (
    RegistrationUserView, SuccessRegistrationView,
    MainPageView, InfoAboutUser, AddArticleView,
    DisplayAllArticlesView, DisplayArticlesByUser,
    UserInfoUpdateView, 
    PostEditView,
    )


urlpatterns = [
    path('blog/', MainPageView, name='main_page'),
    path('blog/user/', InfoAboutUser, name='information'),
    path('login/', decorators.axes_dispatch(auth_views.LoginView.as_view()), name='login'),
    path('blog/user/add_articles/', AddArticleView.as_view(), name='add_article'),
    path('blog/user/edit/', UserInfoUpdateView.as_view(), name='edit_info'),
    path('blog/user/change_password/', auth_views.PasswordChangeView.as_view(template_name='info/ch_psswd.html',
                                                                             success_url=reverse_lazy('main_page')), name='change-password'),
    path('blog/user/<str:user_articles>/', DisplayArticlesByUser.as_view(), name='user_articles'),
    path('blog/<str:name>/', DisplayAllArticlesView.as_view(), name='specific_article'),
    path('blog/user/edit_article/<int:pk>', PostEditView, name='edit_article'),
    path('registration/success/', SuccessRegistrationView, name='sucs_registration'),
    path('registration/', RegistrationUserView.as_view(), name='registration'),
]
