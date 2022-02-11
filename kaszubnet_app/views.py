from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q

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
        request.session['active_character'] = character_name
        character = Character.objects.get(name=character_name)
        return render(request, "main_menu.html", {"current_url": current_url, "character": character})


class FactionMenuView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        current_url = request.path

        character_name = request.session['active_character']
        character = Character.objects.get(name=character_name)
        return render(request, "faction_menu.html", {"current_url": current_url, "character": character})


class FactionMembersView(LoginRequiredMixin, TemplateView):
    template_name = "faction_members.html"
    context_object_name = "members"

    def get_context_data(self, **kwargs):
        context = super(FactionMembersView, self).get_context_data(**kwargs)
        context['alive_members'] = Character.objects.filter(Q(dead=False) & ~Q(rank=3) & Q(left_faction=False))
        context['recruits'] = Character.objects.filter(rank=3)
        context['dead_members'] = Character.objects.filter(Q(dead=True) & Q(left_faction=False))
        context['left_members'] = Character.objects.filter(left_faction=True)
        return context


class FactionHierarchyView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, "faction_hierarchy.html")


class FactionLawView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, "faction_law.html")


class ChronicleMenuView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, "chronicle_menu.html")


class ChronicleChronologyView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, "chronicle_chronology.html")


class ExpansionMapView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, "expansion_map.html")
