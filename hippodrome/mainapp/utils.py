from datetime import datetime, date, time

from django.shortcuts import redirect
from django.template.defaulttags import url
from django.urls import reverse

from .models import Owner, Jockey, Profile, Couple, Race, Hippodrome, Horse

visitors_menu = [
    {'pk': 0, 'title': "Заглавная", 'url_name': 'races_list'},
    {'pk': 1, 'title': "Список лошадей", 'url_name': 'horses_list'},
    {'pk': 2, 'title': "Список жокеев", 'url_name': 'jockeys_list'},
    {'pk': 3, 'title': "Список владельцев", 'url_name': 'owners_list'},
]

admin_menu = [
    {'pk': 0, 'title': "Заглавная", 'url_name': 'races_list'},
    {'pk': 1, 'title': "Список лошадей", 'url_name': 'horses_list'},
    {'pk': 2, 'title': "Список жокеев", 'url_name': 'jockeys_list'},
    {'pk': 3, 'title': "Список владельцев", 'url_name': 'owners_list'},
    {'pk': 4, 'title': "Список печати", 'url_name': 'reports_list'},
]

def get_side_menu(_request):
    if _request.user.is_superuser == False:
        return visitors_menu
    else:
        return admin_menu


def get_list_v(*kwargs):
    list_v = []
    v_id = 0
    for v in kwargs:
        obj = dict(name=v[0], title=v[1], records=[], id=v_id)
        v_id += 1
        for o in v[2].objects.all():
            if not v[3]:
                obj['records'].append(dict(pk=o.id, value=o.__str__()))
            else:
                obj['records'].append(dict(pk=o.id, photo=o.city.photo.url, value=o.__str__()))

        list_v.append(obj)

    return list_v

def get_self_account(_request):
    if _request.user.is_superuser:
        return 'admin/'
    profile = Profile.objects.filter(user=_request.user.id)
    if profile.exists():
        if Owner.objects.filter(user=profile[0].id).exists():
            return reverse('owner_id', args=[ Owner.objects.get(user=profile[0].id).id ])
        if Jockey.objects.filter(user=profile[0].id).exists():
            return reverse('jockey_id', args=[ Jockey.objects.get(user=profile[0].id).id ])

def get_default_context(request, record=-1):
    return {
        'self_account':get_self_account(request),
        'side_menu': get_side_menu(request),
        'rule_edit': request.user.id == record,
        'punkt_selected': -1,
        'is_login': request.user.is_authenticated,
        'is_admin': request.user.is_superuser,
        'list_v': [],
        'photo': '',
    }


def replace_null(dic, row=''):
    ret_dic = {}
    for key in dic.keys():
        if dic[key] == '':
            if key in ['couple-'+row+'-3', 'time_begin', 'time_end']:
                ret_dic[key] = '00:00'
            if key in ['date']:
                ret_dic[key] = '1900-01-01'
            if key in ['couple-'+row+'-0', 'couple-'+row+'-1', 'hippodrome']:
                ret_dic[key] = '-1'
            if key in ['couple-'+row+'-2', 'distance', 'summa']:
                ret_dic[key] = '0'
        else:
            ret_dic[key] = dic[key]
    return ret_dic

def save_race(d, record=-1):
    list_couples = {}
    race_context = {}
    dic = replace_null(d)
    for key in dic.keys():
        if key.startswith("couple-"):
            str_key = key.split("-")
            r = str_key[1]
            c = str_key[2]
            rdic = replace_null(dic, r)
            if r not in list_couples.keys():
                list_couples[r] = { 'result':0, 'time':time(0) }
            if c == '0':
                list_couples[r]['horse'] = Horse.objects.get(id=int(rdic[key]))
            if c == '1':
                list_couples[r]['jockey'] = Jockey.objects.get(id=int(rdic[key]))
            if c == '2':
                list_couples[r]['result'] = int(rdic[key])
            if c == '3':
                list_couples[r]['time'] = datetime.strptime(rdic[key], "%H:%M").time()

        else:
            if key in ['distance', 'summa']:
                race_context[key] = int(dic[key])
            elif key in ['hippodrome']:
                race_context[key] = Hippodrome.objects.get(id=int(dic[key]))
            elif key in ['date']:
                race_context[key] = datetime.strptime(dic[key], "%Y-%m-%d").date()
            elif key in ['time_begin', 'time_end']:
                race_context[key] = datetime.strptime(dic[key], "%H:%M").time()
            elif key in ['csrfmiddlewaretoken']:
                continue
            else:
                race_context[key] = dic[key]

    if record != -1:
        edit_race = Race(id=record, **race_context)
    else:
        edit_race = Race(**race_context)
    edit_race.save()

    Couple.objects.filter(race=edit_race.id).delete()
    for key in list_couples.keys():
        Couple.objects.create(race=edit_race, **list_couples[key])

    return edit_race.id

