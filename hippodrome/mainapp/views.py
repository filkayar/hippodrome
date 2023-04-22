from datetime import datetime, timedelta, date, time

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import logout, login
from django.views.generic import ListView, DetailView, CreateView, FormView

# Create your views here.
# from .forms import *
from .models import *
from .utils import *


def LoginUser(request):
    pass
def LogoutUser(request):
    pass
def RacesList(request):
    objs = Race.objects.all()
    elem_table = []
    desc_table = ['Дата', 'Время начала', 'Заголовок', 'Город', 'Ипподром']
    for o in objs:
        elem_table.append([
            {
                'type': 'text',
                'value': o.date,
                'link': ''
            },
            {
                'type': 'text',
                'value': o.time_begin,
                'link': ''
            },
            {
                'type': 'link',
                'value': o.title,
                'link': o.get_absolute_url()
            },
            {
                'type': 'text',
                'value': o.hippodrome.city.name,
                'link': ''
            },
            {
                'type': 'text',
                'value': o.hippodrome.name,
                'link': ''
            },
        ])
    side_menu = []
    if request.user.is_superuser == False:
        side_menu = visitors_menu
    else:
        side_menu = admin_menu

    context = {
        'title':'Главная. Список заездов',
        'title_table':'Список заездов',
        'add_record':'race_new',
        'side_menu':side_menu,
        'punkt_selected':0,
        'elem_table':elem_table,
        'desc_table':desc_table,
        'is_login': request.user.is_authenticated,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'mainapp/list.html', context=context)
def HorsesList(request):
    objs = Horse.objects.all()
    elem_table = []
    desc_table = ['Кличка', 'Масть', 'Возраст', 'Собственник']
    for o in objs:
        elem_table.append([
            {
                'type': 'link',
                'value': o.name,
                'link': o.get_absolute_url()
            },
            {
                'type': 'text',
                'value': o.mast,
                'link': ''
            },
            {
                'type': 'text',
                'value': o.age,
                'link': ''
            },
            {
                'type': 'text',
                'value': o.owner.user.__str__(),
                'link': o.get_absolute_url()
            },
        ])
    side_menu = []
    if request.user.is_superuser == False:
        side_menu = visitors_menu
    else:
        side_menu = admin_menu

    context = {
        'title': 'Список лошадей',
        'title_table': 'Список лошадей',
        'add_record': 'horse_new',
        'side_menu': side_menu,
        'punkt_selected': 1,
        'elem_table': elem_table,
        'desc_table': desc_table,
        'is_login': request.user.is_authenticated,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'mainapp/list.html', context=context)
def JockeysList(request):
    objs = Jockey.objects.all()
    elem_table = []
    desc_table = ['ФИО', 'Категория', 'Город']
    for o in objs:
        elem_table.append([
            {
                'type': 'link',
                'value': o.user.__str__(),
                'link': o.get_absolute_url()
            },
            {
                'type': 'text',
                'value': o.category,
                'link': ''
            },
            {
                'type': 'text',
                'value': o.user.city.name,
                'link': ''
            },
        ])
    side_menu = []
    if request.user.is_superuser == False:
        side_menu = visitors_menu
    else:
        side_menu = admin_menu

    context = {
        'title': 'Список жокеев',
        'title_table': 'Список жокеев',
        'add_record': 'jockey_new',
        'side_menu': side_menu,
        'punkt_selected': 2,
        'elem_table': elem_table,
        'desc_table': desc_table,
        'is_login': request.user.is_authenticated,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'mainapp/list.html', context=context)
def OwnersList(request):
    objs = Owner.objects.all()
    elem_table = []
    desc_table = ['ФИО', 'Город']
    for o in objs:
        elem_table.append([
            {
                'type': 'link',
                'value': o.user.__str__(),
                'link': o.get_absolute_url()
            },
            {
                'type': 'text',
                'value': o.user.city.name,
                'link': ''
            },
        ])
    side_menu = []
    if request.user.is_superuser == False:
        side_menu = visitors_menu
    else:
        side_menu = admin_menu

    context = {
        'title': 'Список владельцев',
        'title_table': 'Список владельцев',
        'add_record': 'owner_new',
        'side_menu': side_menu,
        'punkt_selected': 3,
        'elem_table': elem_table,
        'desc_table': desc_table,
        'is_login': request.user.is_authenticated,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'mainapp/list.html', context=context)
def RepportsList(request):
    if request.user.is_superuser == False:
        side_menu = visitors_menu
    else:
        side_menu = admin_menu

    context = {
        'title': 'Список печати',
        'title_table': 'Список печати',
        'side_menu': side_menu,
        'punkt_selected': 4,
        'is_login': request.user.is_authenticated,
    }
    return render(request, 'mainapp/reports.html', context=context)

def RaceId(request, record):
    rec = get_object_or_404(Race, id=record)
    now = datetime.now()

    status = ''
    tb = datetime(year=rec.date.year, month=rec.date.month, day=rec.date.day, hour=rec.time_begin.minute, minute=rec.time_begin.minute, second=0)
    te = datetime(year=rec.date.year, month=rec.date.month, day=rec.date.day, hour=rec.time_end.minute, minute=rec.time_end.minute, second=0)

    if now >= tb :
        status = 'Завершен'
    if now < tb :
        status = 'Ожидается'
    if now < te and now >= tb :
        status = 'В процессе'

    couples = Couple.objects.filter(race=rec.id)

    if request.user.is_superuser == False:
        side_menu = visitors_menu
    else:
        side_menu = admin_menu
    context = {
        'title': 'Заезд: '+rec.title,
        'title_race': rec.title,
        'side_menu': side_menu,
        'punkt_selected': -1,
        'is_login': request.user.is_authenticated,
        'is_admin': request.user.is_superuser,

        'city':rec.hippodrome.city.__str__(),
        'hippodrome':rec.hippodrome.__str__(),
        'status':status,
        'date':rec.date,
        'time_begin':rec.time_begin.strftime("%H:%M"),
        'time_end':rec.time_end.strftime("%H:%M"),
        'distance':rec.distance,
        'summa':rec.summa,
        'count_couples':len(couples),
        'org':rec.org,
        'couples':couples,
        'photo': rec.hippodrome.city.photo.url,
        'edit_url': reverse('race_edit', args=[rec.id])
    }
    return render(request, 'mainapp/race.html', context=context)
def JockeyId(request):
    pass
def HorseId(request):
    pass
def OwnerId(request):
    pass

def RaceEdit(request, record):
    if request.user.is_superuser == False:
        side_menu = visitors_menu
    else:
        side_menu = admin_menu

    rec = get_object_or_404(Race, id=record)

    couples = []
    for c in Couple.objects.filter(race=rec.id):
        i = len(couples)
        couples.append({
            'rec':c,
            'pk':i
        })

    dict_horses = []
    dict_jockeys = []
    dict_cities = []
    dict_hippodrome = []

    for h in Horse.objects.all():
        dict_horses.append(dict(pk=h.id, name=h.__str__()))
    for j in Jockey.objects.all():
        dict_jockeys.append(dict(pk=j.id, name=j.__str__()))
    for c in City.objects.all():
        dict_cities.append(dict(pk=c.id, photo=c.photo.url, name=c.__str__()))
    for h in Hippodrome.objects.all():
        dict_hippodrome.append(dict(pk=h.id, name=h.__str__()))

    context = {
        'title': 'Заезд: ' + rec.title,
        'side_menu': side_menu,
        'punkt_selected': -1,
        'is_login': request.user.is_authenticated,

        'new_records':False,
        'dict_horses':dict_horses,
        'dict_jockeys':dict_jockeys,
        'dict_cities':dict_cities,
        'dict_hippodrome':dict_hippodrome,

        'photo':rec.hippodrome.city.photo.url,


        'city': rec.hippodrome.city.__str__(),
        'city_pk': rec.hippodrome.city.id,
        'hippodrome': rec.hippodrome.__str__(),
        'hippodrome_pk': rec.hippodrome.id,

        'title_race': rec.title,
        'date': rec.date.strftime("%Y-%m-%d"),
        'time_begin':rec.time_begin.strftime("%H:%M"),
        'time_end':rec.time_end.strftime("%H:%M"),
        'distance': rec.distance,
        'summa': rec.summa,
        'org': rec.org,

        'couples': couples
    }
    return render(request, 'mainapp/race_input_edit.html', context=context)
def HorseEdit(request):
    pass
def JockeyEdit(request):
    pass
def OwnerEdit(request):
    pass


def RaceNew(request):
    pass
def JockeyNew(request):
    pass
def HorseNew(request):
    pass
def OwnerNew(request):
    pass
