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

from axes import decorators
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .views import (
    RegistrationUser,
    main_page,
    info_about_user,
    AddArticle,
    DisplayAllArticles,
    DisplayArticlesByUser,
    UserInfoUpdate,
    post_edit_view,
    CustomLoginView,
    CheckPinView,
)

urlpatterns = [
    path('', decorators.axes_dispatch(CustomLoginView.as_view()), name='login'),
    path('blog/', main_page, name='main_page'),
    path('blog/user/', info_about_user, name='information'),
    path('login/', decorators.axes_dispatch(CustomLoginView.as_view()), name='login'),
    path('login/code-authenticate/', decorators.axes_dispatch(CheckPinView.as_view()), name='verify'),
    path('blog/user/add_article/', AddArticle.as_view(), name='add_article'),
    path('blog/user/edit/', UserInfoUpdate.as_view(), name='edit_info'),
    path('blog/user/change_password/',
         auth_views.PasswordChangeView.as_view(
             template_name='info/ch_psswd.html',
             success_url=reverse_lazy('main_page')),
         name='change-password'),
    path('blog/user/<str:user_articles>/', DisplayArticlesByUser.as_view(), name='user_articles'),
    path('blog/<str:name>/', DisplayAllArticles.as_view(), name='specific_article'),
    path('blog/user/edit_article/<int:pk>', post_edit_view, name='edit_article'),
    path('registration/', RegistrationUser.as_view(), name='registration'),
]
