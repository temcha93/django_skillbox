from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse

from app_users.models import Profile


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect(reverse('account', args=[user.pk]))
    else:
        form = UserCreationForm()
    return render(request, "app_users/register.html", {'form': form})


def account_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if request.user.has_perm('app_users.set_verified'):
            profile = user.profile
            profile.is_author = True
            profile.save()
    return render(request, "app_users/account.html", {'user': user})


class LoginView(LoginView):
    template_name = 'app_users/login.html'


class LogoutView(LogoutView):
    next_page = '/'


@method_decorator([login_required], name='dispatch')
class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'app_users/update_profile.html'
    fields = ['name', 'last_name', 'about', 'phone', 'city', 'avatar']

    def dispatch(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        if not profile.user == request.user:  # для предотвращения редактирования чужого профиля
            return HttpResponseRedirect(reverse('edit_profile', args=[request.user.profile.pk]))
        return super().dispatch(request, pk, *args, **kwargs)
