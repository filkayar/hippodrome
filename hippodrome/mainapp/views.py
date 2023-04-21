from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import logout, login
from django.views.generic import ListView, DetailView, CreateView, FormView

# Create your views here.
# from .forms import *
from .models import *
from .utils import *

class RacesList(DataMixin, ListView):
    pass

class HorsesList(DataMixin, ListView):
    pass

class JockeysList(DataMixin, ListView):
    pass

class OwnersList(DataMixin, ListView):
    pass

class RepportsList(DataMixin, ListView):
    pass


class RaceId(DataMixin, DetailView):
    pass

class JockeyId(DataMixin, DetailView):
    pass

class HorseId(DataMixin, DetailView):
    pass

class OwnerId(DataMixin, DetailView):
    pass


class RaceEdit(DataMixin, FormView):
    pass

class HorseEdit(DataMixin, FormView):
    pass
class JockeyEdit(DataMixin, FormView):
    pass
class OwnerEdit(DataMixin, FormView):
    pass


class RaceNew(DataMixin, CreateView):
    pass

class JockeyNew(DataMixin, CreateView):
    pass

class HorseNew(DataMixin, CreateView):
    pass

class OwnerNew(DataMixin, CreateView):
    pass
