from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic.edit import CreateView
from django.views import View
from django.views.generic import UpdateView
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from first_blood.settings import authy_api, country_code_twilio 
from .forms import UserForm, AddArticleForm, UpdateInfoForm, PinForm
from .models import Article, User_Profile


class RegistrationUserView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('main_page')
    template_name ='add/register_per.html'


@login_required
def SuccessRegistrationView(request):
    return TemplateResponse(request, 'add/registered_per.html')


def MainPageView(request):
    Articles = Article.objects.all()
    return TemplateResponse(request, 'main.html', {'Articles': Articles})


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
                if not  request_sms.ok():
                    return HttpResponseBadRequest('Sorry! Some troubles with number!')
                else:
                    self.request.session['auth_user'] = username
                    return  redirect('verify')
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})

           
class CheckPinView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        form = PinForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = PinForm(request.POST)
        if 'auth_user' in request.session:
            name = request.session['auth_user']
            user = get_object_or_404(User_Profile, username=name)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            if pin:
                check = authy_api.phones.verification_check(user.phone, country_code_twilio, pin)
                if check.ok():
                    login(request, user)
                    return redirect('main_page')
                else:
                    return redirect('main_page')
        else:
            form = PinForm()
            return render(request, 'registration/login.html', {'form': form})
        

@login_required
def InfoAboutUser(request):
    current_time = now()
    return TemplateResponse(request, 'info/info.html', {'c_time': current_time})


@method_decorator(login_required, name='dispatch')
class AddArticleView(CreateView):
    template_name = 'articles/adding_articles.html'
    form_class = AddArticleForm

    def post(self, request, *args, **kwargs):
        form = AddArticleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return  redirect('main_page')
        else:
            form = AddArticleForm()
        return render(request, 'articles/adding_articles.html', {'form': form})

    
class DisplayAllArticlesView(TemplateView):
    template_name = 'articles/all_articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Articles'] = Article.objects.filter(title=kwargs['name'])
        return context


class DisplayArticlesByUser(TemplateView):
    template_name = 'articles/current_articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Articles'] = Article.objects.filter(author__username=kwargs['user_articles'])
        return context


class UserInfoUpdateView(UpdateView):
    form_class = UpdateInfoForm
    template_name = 'info/edit_info.html'
    success_url = reverse_lazy('information')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)


@login_required
def PostEditView(request, pk):
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
    return render(request, 'articles/edit_article.html',{'form': form} )
