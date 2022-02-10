from django.views import View
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from kaszubnet_app.forms import LoginForm
from kaszubnet_app.models import *


class IndexView(View):
    def get(self, request):
        form = LoginForm
        return render(request, "index.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            print(user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/user_menu/')
            return render(request, "index.html", {"form": form})
        return render(request, "index.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("/index")


class UserMenuView(LoginRequiredMixin, ListView):
    model = Character

    template_name = "user_menu.html"
    context_object_name = "character"

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user.id)

    def get_context_data(self, **kwargs):
        # cmr_id = self.kwargs["id"]
        context = super().get_context_data(**kwargs)
        # context["cmr"] = get_object_or_404(Character, id=cmr_id)
        return context


class MainMenuView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        current_url = request.path

        character_name = self.kwargs["name"]
        character = Character.objects.get(name=character_name)
        return render(request, "main_menu.html", {"current_url": current_url, "character": character})
