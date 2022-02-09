from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from kaszubnet_app.forms import LoginForm


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


class UserMenuView(View):
    def get(self, request):
        return render(request, "user_menu.html")
