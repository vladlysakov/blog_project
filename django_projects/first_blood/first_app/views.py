from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import View
from django.views.generic import UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .credentials.twilio import country_code_twilio, authy_api

from .forms import UserForm, AddArticleForm, UpdateInfoForm, PinForm
from .models import Article, User_Profile


class RegistrationUser(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('main_page')
    template_name = 'add/registration.html'


@login_required
def success_registration(request):
    return TemplateResponse(request, 'add/registered_per.html')


def main_page(request):
    articles = Article.objects.all()
    content = []

    for article in articles:
        result_article = {}

        if len(article.content) > 100:
            result_article['content'] = article.content[:100]
        else:
            result_article['content'] = article.content

        result_article['title'] = article.title
        content.append(result_article)

    return TemplateResponse(request, 'articles/articles.html', {'articles': content})


class CustomLoginView(View):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm

    def get(self, request):
        form = AuthenticationForm()

        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            auth_user = authenticate(username=username, password=password)

            if auth_user is not None:
                request_sms = authy_api.phones.verification_start(auth_user.phone, country_code_twilio, via='sms')

                if not request_sms.ok():
                    return HttpResponseBadRequest('Sorry! Some troubles with number!')
                else:
                    self.request.session['auth_user'] = username
                    return redirect('verify')
        else:
            form = AuthenticationForm()

            return render(request, 'registration/login.html', {'form': form})


class CheckPinView(View):
    template_name = 'registration/pin.html'

    def get(self, request):
        form = PinForm()

        return render(request, 'registration/pin.html', {'form': form})

    def post(self, request):
        form = PinForm(request.POST)
        user = get_object_or_404(User_Profile, username=request.session['auth_user'])

        if form.is_valid():
            pin = form.cleaned_data['pin']

            if pin and user:
                check = authy_api.phones.verification_check(user.phone, country_code_twilio, pin)

                if check.ok():
                    login(request, user)

                    return redirect('main_page')
                else:
                    return redirect('verify')
        else:
            form = PinForm()

            return render(request, 'registration/login.html', {'form': form})


@login_required
def info_about_user(request):
    current_time = now()

    return TemplateResponse(request, 'info/info.html', {'c_time': current_time})


@method_decorator(login_required, name='dispatch')
class AddArticle(CreateView):
    template_name = 'articles/add_article.html'
    form_class = AddArticleForm

    def post(self, request, *args, **kwargs):
        form = AddArticleForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('main_page')
        else:
            form = AddArticleForm()

        return render(request, 'articles/add_article.html', {'form': form})


class DisplayAllArticles(TemplateView):
    template_name = 'articles/specific_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(title=kwargs['name'])

        return context


class DisplayArticlesByUser(TemplateView):
    template_name = 'articles/articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(author__username=kwargs['user_articles'])

        return context


class UserInfoUpdate(UpdateView):
    form_class = UpdateInfoForm
    template_name = 'info/edit_info.html'
    success_url = reverse_lazy('information')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Article, id=pk)

    if request.method == "POST":

        if post.author != request.user:
            return HttpResponseForbidden("You don't have permission")
        else:
            form = AddArticleForm(request.POST, instance=post)

            if form.is_valid():
                post = form.save()
                post.save()

                return redirect('information')
    else:
        form = AddArticleForm(instance=post)

    return render(request, 'articles/edit_article.html', {'form': form})
