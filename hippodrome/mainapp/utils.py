from datetime import datetime, time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.template.loader import get_template
from django.urls import reverse
import pdfkit

from .models import Owner, Jockey, Profile, Couple, Race, Hippodrome, Horse, City

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
    profile = Profile.objects.filter(user=_request.user.id)
    if profile.exists():
        if Owner.objects.filter(user=profile[0].id).exists():
            return reverse('owner_id', args=[ Owner.objects.get(user=profile[0].id).id ])
        if Jockey.objects.filter(user=profile[0].id).exists():
            return reverse('jockey_id', args=[ Jockey.objects.get(user=profile[0].id).id ])
    return '#'

def get_default_context(request, record=-1):
    return {
        'add_record': 'owner_new',
        'self_account':get_self_account(request),
        'side_menu': [
            {'pk': 0, 'title': "Заглавная", 'url_name': 'races_list'},
            {'pk': 1, 'title': "Список лошадей", 'url_name': 'horses_list'},
            {'pk': 2, 'title': "Список жокеев", 'url_name': 'jockeys_list'},
            {'pk': 3, 'title': "Список владельцев", 'url_name': 'owners_list'},
            {'pk': 4, 'title': "Список печати", 'url_name': 'reports_list'},
        ],
        'rule_edit': request.user.id == record or request.user.is_superuser,
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
            if key in ['date', 'birth', 'd_passport', 'dn']:
                ret_dic[key] = '1900-01-01'
            if key in ['de']:
                ret_dic[key] = '2045-05-09'
            if key in ['couple-'+row+'-0', 'couple-'+row+'-1', 'hippodrome', 'city', 'owner', 'race', 'horse', 'jockey']:
                ret_dic[key] = '-1'
            if key in ['couple-'+row+'-2', 'distance', 'summa', 's_passport', 'n_passport', 'age', 'report']:
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

def save_horse(d, record):
    horse = Horse.objects.get(id=record)
    dic = replace_null(d.POST)

    horse.name = dic['name']
    horse.mast = dic['mast']
    horse.age = int(dic['age'])
    horse.owner = Owner.objects.get(id=int(dic['owner']))

    if d.FILES:
        if horse.photo:
            horse.photo.delete(False)
        file = d.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save('photos/horse/'+datetime.now().year.__str__()+'/'+datetime.now().month.__str__()+'/'+datetime.now().day.__str__()+'/'+file.name, file)
        horse.photo = filename

    horse.save()

    return horse.id
def save_user(d, record, obj):
    acc = obj.objects.get(id=record)
    prof = Profile.objects.get(id= acc.user.id)
    usr = User.objects.get(id=prof.user.id)

    dic = replace_null(d.POST)

    prof.s_passport = int(dic['s_passport'])
    prof.n_passport = int(dic['n_passport'])
    usr.first_name = dic['first_name']
    usr.last_name = dic['last_name']
    usr.email = dic['email']
    prof.middle_name = dic['middle_name']
    prof.phone = dic['phone']
    prof.w_passport = dic['w_passport']
    prof.city = City.objects.get(id=int(dic['city']))
    prof.birth = datetime.strptime(dic['birth'], "%Y-%m-%d").date()
    prof.d_passport = datetime.strptime(dic['d_passport'], "%Y-%m-%d").date()
    if obj == Jockey:
        acc.category = dic['category']

    if d.FILES:
        if prof.photo:
            prof.photo.delete(False)
        file = d.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save('photos/user/'+datetime.now().year.__str__()+'/'+datetime.now().month.__str__()+'/'+datetime.now().day.__str__()+'/'+file.name, file)
        prof.photo = filename

    acc.save()
    prof.save()
    usr.save()

    return acc.id


def get_report(dic):
    template = ''
    rep_resp = {}

    if dic['report'] == 0:
        template = 'reports/report0.html'
        rep_resp = {
            'dn':dic['dn'],
            'de':dic['de'],
        }
        # couple__horse = h.id, couple__result=1,
        resp = []
        horses = Horse.objects.all()
        for h in horses:
            resp.append({
                'name':h.name,
                'owner':h.owner.__str__(),
                'count_all':Race.objects.filter( couple__horse = h.id,  date__gte=dic['dn'] , date__lte=dic['de']).count(),
                'one':Race.objects.filter( couple__horse = h.id, couple__result=1, date__gte=dic['dn'], date__lte=dic['de']).count(),
                'two':Race.objects.filter(couple__horse = h.id, couple__result=2,  date__gte=dic['dn'], date__lte=dic['de']).count(),
                'tree': Race.objects.filter(couple__horse = h.id, couple__result=3, date__gte=dic['dn'], date__lte=dic['de']).count(),
            })
        resp.sort(key=lambda item: (item['one'], item['two'], item['tree']), reverse=True)
        for i in range(len(resp)):
            resp[i]['num'] = i+1

        rep_resp['table'] = resp


    if dic['report'] == 1:
        template = 'reports/report1.html'
        rep_resp = {
            'dn':dic['dn'],
            'de':dic['de'],
        }
        resp = []
        jockeys = Jockey.objects.all()
        for j in jockeys:
            resp.append({
                'fio':j.__str__(),
                'category':j.category,
                'count_all':Couple.objects.filter(jockey=j.id, race__date__gte=dic['dn'], race__date__lte=dic['de']).count(),
                'one':Couple.objects.filter(jockey=j.id, result=1, race__date__gte=dic['dn'], race__date__lte=dic['de']).count(),
                'two':Couple.objects.filter(jockey=j.id, result=2, race__date__gte=dic['dn'], race__date__lte=dic['de']).count(),
                'tree': Couple.objects.filter(jockey=j.id, result=3, race__date__gte=dic['dn'],
                                             race__date__lte=dic['de']).count(),
            })
        resp.sort(key=lambda item: (item['one'], item['two'], item['tree']))
        for i in range(len(resp)):
            resp[i]['num'] = i

        rep_resp['table'] = resp


    if dic['report'] == 2 and dic['jockey'] != '':
        dic['jockey'] = dic['jockey'][0]
        template = 'reports/report2.html'
        rep_resp = {
            'fio':dic['jockey'].__str__(),
            'city':dic['jockey'].user.city.__str__(),
            'category':dic['jockey'].category,

            'dn': dic['dn'],
            'de': dic['de'],
        }
        resp = []
        couples = Couple.objects.filter(race__date__gte=dic['dn'], race__date__lte=dic['de'], jockey=dic['jockey'].id)
        for c in couples:
            resp.append({
                'date':c.race.date,
                'race':c.race.__str__(),
                'horse':c.horse.__str__(),
                'distance':c.race.distance,
                'result':c.result,
            })
        resp.sort(key=lambda item: (item['date']))
        rep_resp['table'] = resp


    if dic['report'] == 3 and dic['horse'] != '':
        dic['horse'] = dic['horse'][0]
        template = 'reports/report3.html'
        rep_resp = {
            'name':dic['horse'].name,
            'mast':dic['horse'].mast,
            'owner':dic['horse'].owner.__str__(),
            'age':dic['horse'].age,

            'dn': dic['dn'],
            'de': dic['de'],
        }
        resp = []
        couples = Couple.objects.filter(race__date__gte=dic['dn'], race__date__lte=dic['de'], horse=dic['horse'].id)
        for c in couples:
            resp.append({
                'date':c.race.date,
                'race':c.race.__str__(),
                'jockey':c.jockey.__str__(),
                'distance':c.race.distance,
                'result':c.result,
            })
        resp.sort(key=lambda item: (item['date']))
        rep_resp['table'] = resp


    if dic['report'] == 4:
        template = 'reports/report4.html'
        rep_resp = {
            'dn': dic['dn'],
            'de': dic['de'],
        }
        resp = []
        races = Race.objects.filter(date__gte=dic['dn'], date__lte=dic['de'])
        for r in races:
            resp.append({
                'date':r.date,
                'race':r.__str__(),
                'count':Couple.objects.filter(race=r.id).count(),
                'summa':r.summa,
                'horse':Horse.objects.filter(couple__race__id=r.id, couple__result=1)[0].__str__() if  Horse.objects.filter(couple__race__id=r.id, couple__result=1).exists() else '',
                'jockey':Jockey.objects.filter(couple__race__id=r.id, couple__result=1)[0].__str__() if  Jockey.objects.filter(couple__race__id=r.id, couple__result=1).exists() else '',
            })
        resp.sort(key=lambda item: (item['date']))
        rep_resp['table'] = resp


    if dic['report'] == 5 and dic['race'] != '':
        dic['race'] = dic['race'][0]
        template = 'reports/report5.html'
        rep_resp = {
            'title': dic['race'].__str__(),
            'org': dic['race'].org,
            'date': dic['race'].date,
            'time_begin': dic['race'].time_begin,
            'time_end': dic['race'].time_end,
            'distance': dic['race'].distance,
            'summa': dic['race'].summa,
        }
        resp = []
        couples = Couple.objects.filter(race=dic['race'].id)
        for c in couples:
            resp.append({
                'horse':c.horse.__str__(),
                'jockey':c.jockey.__str__(),
                'result':c.result,
                'time':c.time,
            })
        resp.sort(key=lambda item: (item['result']))
        rep_resp['table'] = resp

    return template, rep_resp

def render_pdf(url_template, contexto):
    template = get_template(url_template)
    html = template.render(contexto)

    return pdfkit.from_string(
        html,
        False,
        options={  'encoding': "utf-8", },
        configuration=pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH),
        css=settings.STATIC_ROOT + "/mainapp/css/reports.css"
    )