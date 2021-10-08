from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from ThietLapNamHocMoi.models import HuynhTruong
from django.contrib.auth import authenticate, logout, login
from django.urls import reverse
from .forms import RegistrationForm, UpdateHTForm, UpdateLoginInfoForm

# Create your views here.
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('Base:dashboard'))
        else:
            return render(request, 'HomePage/login.html')
    def post(self, request):
        username = request.POST.get('InputUsername')
        password = request.POST.get('InputPassword')
        next_url = request.POST.get('next')
        login_user = authenticate(username=username, password=password)
        if login_user is None:
            return render(request, 'HomePage/login.html', {"LoginFail": "1"})
        login(request, login_user)
        return redirect(next_url)
    def logout(request):
        logout(request=request)
        return render(request, 'HomePage/login.html')

class RegistView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'HomePage/register.html', {'form': form})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            HuynhTruong.objects.create_user(username=form.cleaned_data['email'], email=form.cleaned_data['email'], password=form.cleaned_data['password']
                                                , last_name=form.cleaned_data['last_name'], first_name=form.cleaned_data['first_name'],is_active=False)
            return render(request, 'HomePage/successfulregistration.html')
        return render(request, 'HomePage/register.html', {'form': form})

class HomePageView(LoginRequiredMixin,View):
    login_url = '/logout/'
    def get(self, request):
        return render(request, 'HomePage/index.html')

class UpdateHT(LoginRequiredMixin,View):
    login_url = '/logout/'
    def get(self, request):
        form = UpdateHTForm(instance=request.user, request=request)
        form2 = UpdateLoginInfoForm(request=request)
        return render(request, 'HomePage/CapNhatHuynhTruong.html', {'form': form, 'form2': form2})
    def post(self, request):
        form = UpdateHTForm(request.POST, request.FILES, instance=request.user, request=request)
        form2 = UpdateLoginInfoForm(request=request)
        if form.is_valid():
            form.save()
            return redirect(reverse('Base:dashboard'))
        return render(request, 'HomePage/CapNhatHuynhTruong.html', {'form': form, 'form2': form2})
    def UpdateLoginInfo(request):
        form = UpdateHTForm(instance=request.user, request=request)
        form2 = UpdateLoginInfoForm(request.POST, request=request)
        if form2.is_valid():
            objHuynhTruong = HuynhTruong.objects.get(pk=request.user.id_HuynhTruong)
            objHuynhTruong.username = form2.cleaned_data['username']
            objHuynhTruong.set_password(form2.cleaned_data['password'])
            objHuynhTruong.save()
            return redirect(reverse('Base:dashboard'))
        return render(request, 'HomePage/CapNhatHuynhTruong.html', {'form': form, 'form2': form2})