from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from app_users.forms import RegisterForm
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView


class RegisterUserView(View):

    def get(self, request):
        reg_form = RegisterForm()
        return render(request=request, template_name='app_users/register.html', context={'reg_form': reg_form})

    def post(self, request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():

            user = reg_form.save()
            user.refresh_from_db()

            user.city = reg_form.cleaned_data.get('city')
            user.date_of_birth = reg_form.cleaned_data.get('date_of_birth')

            user.save()

            username = reg_form.cleaned_data.get('username')
            password = reg_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            reg_form = RegisterForm()
        return render(request, 'app_users/register.html', {'reg_form': reg_form})

class LoginUserView(LoginView):
    template_name = 'app_users/login.html'
    redirect_authenticated_user = True

class LogoutUserView(LogoutView):
    next_page = '/'
