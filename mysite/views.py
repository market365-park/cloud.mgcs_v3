# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, UpdateView
from django.views.generic.edit import CreateView

from .forms import RegisterForm, ProfileUpdateForm
from .models import User

class MyLoginRequiredMixinView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

class HomeView(MyLoginRequiredMixinView, TemplateView):
    template_name = 'home.html'

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    # model = User
    # queryset = User
    form_class = ProfileUpdateForm
    template_name = 'registration/profile_update.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        users = User.objects.all()
        return users
