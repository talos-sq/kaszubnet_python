from django.views import View
from django.views.generic import ListView, TemplateView, FormView, CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.db.models import Q

from kaszubnet_app.forms import *
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
    context_object_name = "characters"

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class ArtefactsMenuView(LoginRequiredMixin, ListView):
    template_name = "artefacts_menu.html"
    context_object_name = "artefacts"

    def get_queryset(self):
        return Artefact.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArtefactView(LoginRequiredMixin, ListView):
    template_name = "artefact.html"
    context_object_name = "artefact_item"

    def get_queryset(self):
        artefact_name = self.kwargs["name"]
        return Artefact.objects.get(name=artefact_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["artefacts"] = Artefact.objects.all()
        return context


class WarehouseMenuView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, "warehouse_menu.html")


class WarehouseStatusView(LoginRequiredMixin, TemplateView):
    template_name = "warehouse_status.html"

    def get_context_data(self, **kwargs):
        context = super(WarehouseStatusView, self).get_context_data(**kwargs)
        context['undefined'] = WarehouseItems.objects.filter(item_type=0)
        context['usable'] = WarehouseItems.objects.filter(item_type=1)
        context['material'] = WarehouseItems.objects.filter(item_type=2)
        context['medical'] = WarehouseItems.objects.filter(item_type=3)
        context['electronics'] = WarehouseItems.objects.filter(item_type=4)

        return context


class WarehouseActionAddView(LoginRequiredMixin, CreateView):
    template_name = "warehouse_action_add.html"
    form_class = WarehouseActionAddForm

    def post(self, request, *args, **kwargs):
        form = WarehouseActionAddForm(request.POST)

        if form.is_valid():
            validated_form = WarehouseItems.objects.create(**form.cleaned_data)
            return redirect("../warehouse_status/")
        else:
            return redirect("warehouse_action_add/")


class WarehouseActionUpdateView(LoginRequiredMixin, FormView):
    template_name = "warehouse_action_update.html"
    form_class = WarehouseActionUpdateForm

    def get_context_data(self, update_form=None, **kwargs):
        context = super(WarehouseActionUpdateView, self).get_context_data(**kwargs)
        context['update_form'] = update_form if update_form is not None else WarehouseActionUpdateForm()
        return context


class ExpansionMapView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        return render(request, "expansion_map.html")
