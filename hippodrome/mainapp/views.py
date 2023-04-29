from django.shortcuts import render, redirect, get_object_or_404
from .utils import *

def ErrorAccess(request):
    return render(request, 'mainapp/error_access.html', context=get_default_context(request))

def RacesList(request):
    elem_table = []
    for o in Race.objects.all():
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

    context = get_default_context(request)
    custom_context = {
        'title':'Главная. Список заездов',
        'title_table':'Список заездов',
        'is_race': request.user.is_superuser,
        'add_record':'race_new',
        'punkt_selected':0,
        'elem_table':elem_table,
        'desc_table':['Дата', 'Время начала', 'Заголовок', 'Город', 'Ипподром'],
    }
    return render(request, 'mainapp/list.html', context=context|custom_context)

def HorsesList(request):
    elem_table = []
    for o in Horse.objects.all():
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
                'type': 'link',
                'value': o.owner.user.__str__(),
                'link': o.owner.get_absolute_url()
            },
        ])

    context = get_default_context(request)
    custom_context = {
        'title': 'Список лошадей',
        'title_table': 'Список лошадей',
        'is_race': False,
        'punkt_selected': 1,
        'elem_table': elem_table,
        'desc_table': ['Кличка', 'Масть', 'Возраст', 'Собственник'],
    }
    return render(request, 'mainapp/list.html', context=context|custom_context)

def JockeysList(request):
    elem_table = []
    for o in Jockey.objects.all():
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

    context = get_default_context(request)
    custom_context = {
        'title': 'Список жокеев',
        'title_table': 'Список жокеев',
        'is_race': False,
        'punkt_selected': 2,
        'elem_table': elem_table,
        'desc_table': ['ФИО', 'Категория', 'Город'],
    }
    return render(request, 'mainapp/list.html', context=context|custom_context)

def OwnersList(request):
    elem_table = []
    for o in Owner.objects.all():
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

    context = get_default_context(request)
    custom_context = {
        'title': 'Список владельцев',
        'title_table': 'Список владельцев',
        'is_race': False,
        'punkt_selected': 3,
        'elem_table': elem_table,
        'desc_table': ['ФИО', 'Город'],
    }
    return render(request, 'mainapp/list.html', context=context|custom_context)

def RepportsList(request):
    context = get_default_context(request)
    custom_context = {
        'title': 'Список печати',
        'title_table': 'Список печати',
        'punkt_selected': 4,
    }
    return render(request, 'mainapp/reports.html', context=context|custom_context)



def RaceId(request, record):
    rec = get_object_or_404(Race, id=record)

    now = datetime.now()
    tb = datetime(year=rec.date.year, month=rec.date.month, day=rec.date.day, hour=rec.time_begin.hour,
                  minute=rec.time_begin.minute, second=0)
    te = datetime(year=rec.date.year, month=rec.date.month, day=rec.date.day, hour=rec.time_end.hour,
                  minute=rec.time_end.minute, second=0)


    status = ''
    if now >= tb :
        status = 'Завершен'
    if now < tb :
        status = 'Ожидается'
    if now < te and now >= tb :
        status = 'В процессе'

    couples = Couple.objects.filter(race=rec.id)

    context = get_default_context(request)
    custom_context = {
        'title': 'Заезд: '+rec.title,
        'title_race': rec.title,
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
    return render(request, 'mainapp/race.html', context=context|custom_context)

def JockeyId(request, record):
    rec = get_object_or_404(Jockey, id=record)

    d = [
        {'type':'text', 'link':'', 'desc':'ФИО', 'value': rec.__str__()},
        {'type':'text', 'link':'', 'desc':'Категория', 'value': rec.category},
        {'type':'text', 'link':'', 'desc':'Телефон', 'value': rec.user.phone},
        {'type':'text', 'link':'', 'desc':'Электронная почта', 'value': rec.user.user.email},
        {'type':'text', 'link':'', 'desc':'Город', 'value': rec.user.city.__str__()},
        {'type':'text', 'link':'', 'desc':'Дата рождения', 'value': rec.user.birth},
    ]

    elem_table = []
    for c in Couple.objects.filter(jockey=rec.id):
        elem_table.append([
            {
                'type':'text',
                'value':c.race.date,
                'link':''
            },
            {
                'type': 'link',
                'value': c.race.__str__(),
                'link': c.race.get_absolute_url()
            },
            {
                'type': 'link',
                'value': c.horse.__str__(),
                'link': c.horse.get_absolute_url()
            },
            {
                'type': 'text',
                'value': c.race.distance,
                'link': ''
            },
            {
                'type': 'text',
                'value': c.result,
                'link': ''
            },
            {
                'type': 'text',
                'value': c.time,
                'link': ''
            },
        ])

    context = get_default_context(request, rec.user.user.id)
    custom_context = {
        'title': 'Наездник: ' + rec.__str__(),
        'account_name': rec.__str__(),
        'record':d,
        'title_table':'Результаты заездов',
        'desc_table':['Дата', 'Событие', 'Скакун', 'Дистанция', 'Результат', 'Время'],
        'elem_table':elem_table,
        'photo': rec.user.photo.url,
        'edit_url': reverse('jockey_edit', args=[rec.id])
    }
    return render(request, 'mainapp/acc_horse_jokey.html', context=context|custom_context)

def HorseId(request, record):
    rec = get_object_or_404(Horse, id=record)

    d = [
        {'type':'text', 'link':'', 'desc':'Кличка', 'value': rec.__str__()},
        {'type':'text', 'link':'', 'desc':'Масть', 'value': rec.mast},
        {'type':'text', 'link':'', 'desc':'Возраст', 'value': rec.age},
        {'type':'link', 'link':rec.owner.get_absolute_url(), 'desc':'Владелец', 'value': rec.owner.__str__()},
    ]

    elem_table = []
    for c in Couple.objects.filter(horse=rec.id):
        elem_table.append([
            {
                'type':'text',
                'value':c.race.date,
                'link':''
            },
            {
                'type': 'link',
                'value': c.race.__str__(),
                'link': c.race.get_absolute_url()
            },
            {
                'type': 'link',
                'value': c.jockey.__str__(),
                'link': c.jockey.get_absolute_url()
            },
            {
                'type': 'text',
                'value': c.race.distance,
                'link': ''
            },
            {
                'type': 'text',
                'value': c.result,
                'link': ''
            },
            {
                'type': 'text',
                'value': c.time,
                'link': ''
            },
        ])

    context = get_default_context(request)
    custom_context = {
        'title': 'Скакун: ' + rec.__str__(),
        'account_name': rec.__str__(),
        'rule_edit': request.user.is_superuser,
        'record':d,
        'title_table':'Результаты заездов',
        'desc_table':['Дата', 'Событие', 'Жокей', 'Дистанция', 'Результат', 'Время'],
        'elem_table':elem_table,
        'photo': rec.photo.url,
        'edit_url': reverse('horse_edit', args=[rec.id])
    }
    return render(request, 'mainapp/acc_horse_jokey.html', context=context|custom_context)

def OwnerId(request, record):
    rec = get_object_or_404(Owner, id=record)

    d = [
        {'type':'text', 'link':'', 'desc':'ФИО', 'value': rec.__str__()},
        {'type':'text', 'link':'', 'desc':'Телефон', 'value': rec.user.phone},
        {'type':'text', 'link':'', 'desc':'Электронная почта', 'value': rec.user.user.email},
        {'type':'text', 'link':'', 'desc':'Город', 'value': rec.user.city.__str__()},
        {'type':'text', 'link':'', 'desc':'Дата рождения', 'value': rec.user.birth},
    ]

    horses = Horse.objects.filter(owner=record)
    couples = []
    for h in horses:
        for c in Couple.objects.filter(horse=h.id):
            couples.append(c)

    context = get_default_context(request, rec.user.user)
    custom_context = {
        'title': 'Собственник: ' + rec.__str__(),
        'account_name': rec.__str__(),
        'record':d,
        'photo': rec.user.photo.url,
        'edit_url': reverse('owner_edit', args=[rec.id]),
        'horses':horses,
        'couples':couples
    }
    return render(request, 'mainapp/acc_sobstvennik.html', context=context|custom_context)




def RaceEdit(request, record):
    rec = get_object_or_404(Race, id=record)
    if not request.user.is_superuser:
        return redirect('err_access')

    if request.method == 'POST':
        return redirect(reverse('race_id', args=[save_race(request.POST, record)]))

    couples = []
    for c in Couple.objects.filter(race=rec.id):
        i = len(couples)
        couples.append({
            'rec': { 'horse': c.horse, 'jockey':c.jockey, 'result': (c.result or ''), 'time': (c.time or time(0)).strftime("%H:%M") },
            'pk':i
        })

    context = get_default_context(request)
    custom_context = {
        'title': 'Заезд: ' + rec.title,

        'new_records':False,
        'photo':rec.hippodrome.city.photo.url,

        'list_v':get_list_v(
            ['table_hippodrome', 'Ипподромы', Hippodrome, True],
            ['table_horses', 'Лошади', Horse, False],
            ['table_jokey', 'Наездники', Jockey, False],
        ),

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
    return render(request, 'mainapp/race_input_edit.html', context=context|custom_context)

def HorseEdit(request, record):
    rec = get_object_or_404(Horse, id=record)
    if not request.user.is_superuser:
        return redirect('err_access')

    if request.method == 'POST':
        return redirect(reverse('horse_id', args=[save_horse(request, record)]))

    fields = [
        {
            'desc':'Кличка',
            'no_link':True,
            'name':'name',
            'type':'text',
            'value':rec.name,
            'viborka':'',
            'text':'',
        },
        {
            'desc': 'Масть',
            'no_link': True,
            'name': 'mast',
            'type': 'text',
            'value': rec.mast,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Возраст',
            'no_link': True,
            'name': 'age',
            'type': 'number',
            'value': rec.age,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Владелец',
            'no_link': False,
            'name': 'owner',
            'type': '',
            'value': rec.owner.id,
            'viborka': 'owners_table',
            'text': rec.owner.__str__(),
        },
    ]

    context = get_default_context(request)
    custom_context = {
        'title': 'Редактирование аккаунта лошади: ' + rec.__str__(),
        'title_head':rec.__str__(),
        'list_v':get_list_v(['owners_table','Владельцы',Owner,False],),
        'photo':rec.photo.url,
        'fields':fields,
    }
    return render(request, 'mainapp/input_edit_account.html', context=context|custom_context)

def JockeyEdit(request, record):
    rec = get_object_or_404(Jockey, id=record)
    if request.user.id != rec.user.user.id and not request.user.is_superuser:
        return redirect('err_access')

    if request.method == 'POST':
        return redirect(reverse('jockey_id', args=[save_user(request, record, Jockey)]))

    fields = [
        {
            'desc': 'Фамилия',
            'no_link': True,
            'name': 'last_name',
            'type': 'text',
            'value': rec.user.user.last_name,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Имя',
            'no_link': True,
            'name': 'first_name',
            'type': 'text',
            'value': rec.user.user.first_name,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Отчество',
            'no_link': True,
            'name': 'middle_name',
            'type': 'text',
            'value': rec.user.middle_name,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Категория',
            'no_link': True,
            'name': 'category',
            'type': 'text',
            'value': rec.category,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Телефон',
            'no_link': True,
            'name': 'phone',
            'type': 'text',
            'value': rec.user.phone,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Почта',
            'no_link': True,
            'name': 'email',
            'type': 'text',
            'value': rec.user.user.email,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Дата рождения',
            'no_link': True,
            'name': 'birth',
            'type': 'date',
            'value': rec.user.birth.strftime("%Y-%m-%d"),
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Серия паспорта',
            'no_link': True,
            'name': 's_passport',
            'type': 'number',
            'value': rec.user.s_passport,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Номер паспорта',
            'no_link': True,
            'name': 'n_passport',
            'type': 'number',
            'value': rec.user.n_passport,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Дата выдачи паспорта',
            'no_link': True,
            'name': 'd_passport',
            'type': 'date',
            'value': rec.user.d_passport.strftime("%Y-%m-%d"),
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Кем выдан паспорт',
            'no_link': True,
            'name': 'w_passport',
            'type': 'text',
            'value': rec.user.w_passport,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Город',
            'no_link': False,
            'name': 'city',
            'type': '',
            'value': rec.user.city.id,
            'viborka': 'cities_table',
            'text': rec.user.city.__str__(),
        },
    ]

    context = get_default_context(request)
    custom_context = {
        'title': 'Редактирование аккаунта наездника: ' + rec.__str__(),
        'title_head': rec.__str__(),
        'photo': rec.user.photo.url,
        'list_v': get_list_v(['cities_table','Города',City,False],),
        'fields':fields,
    }
    return render(request, 'mainapp/input_edit_account.html', context=context|custom_context)

def OwnerEdit(request, record):
    rec = get_object_or_404(Owner, id=record)
    if request.user.id != rec.user.user.id and not request.user.is_superuser:
        return redirect('err_access')

    if request.method == 'POST':
        return redirect(reverse('owner_id', args=[save_user(request, record, Owner)]))

    fields = [
        {
            'desc': 'Фамилия',
            'no_link': True,
            'name': 'last_name',
            'type': 'text',
            'value': rec.user.user.last_name,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Имя',
            'no_link': True,
            'name': 'first_name',
            'type': 'text',
            'value': rec.user.user.first_name,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Отчество',
            'no_link': True,
            'name': 'middle_name',
            'type': 'text',
            'value': rec.user.middle_name,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Телефон',
            'no_link': True,
            'name': 'phone',
            'type': 'text',
            'value': rec.user.phone,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Почта',
            'no_link': True,
            'name': 'email',
            'type': 'text',
            'value': rec.user.user.email,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Дата рождения',
            'no_link': True,
            'name': 'birth',
            'type': 'date',
            'value': rec.user.birth.strftime("%Y-%m-%d"),
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Серия паспорта',
            'no_link': True,
            'name': 's_passport',
            'type': 'number',
            'value': rec.user.s_passport,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Номер паспорта',
            'no_link': True,
            'name': 'n_passport',
            'type': 'number',
            'value': rec.user.n_passport,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Дата выдачи паспорта',
            'no_link': True,
            'name': 'd_passport',
            'type': 'date',
            'value': rec.user.d_passport.strftime("%Y-%m-%d"),
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Кем выдан паспорт',
            'no_link': True,
            'name': 'w_passport',
            'type': 'text',
            'value': rec.user.w_passport,
            'viborka': '',
            'text': '',
        },
        {
            'desc': 'Город',
            'no_link': False,
            'name': 'city',
            'type': '',
            'value': rec.user.city.id,
            'viborka': 'cities_table',
            'text': rec.user.city.__str__(),
        },
    ]

    context = get_default_context(request)
    custom_context = {
        'title': 'Редактирование аккаунта владельца: ' + rec.__str__(),
        'title_head': rec.__str__(),
        'photo': rec.user.photo.url,
        'list_v':get_list_v(['cities_table','Города',City,False],),
        'fields':fields,
    }
    return render(request, 'mainapp/input_edit_account.html', context=context|custom_context)



def RaceNew(request):
    if not request.user.is_superuser:
        return redirect('err_access')

    if request.method == 'POST':
        return redirect(reverse('race_id', args=[save_race(request.POST)]))
    context = get_default_context(request)
    custom_context = {
        'title':'Новый заезд',

        'new_records': True,
        'list_v': get_list_v(
            ['table_hippodrome', 'Ипподромы', Hippodrome, True],
            ['table_horses', 'Лошади', Horse, False],
            ['table_jokey', 'Наездники', Jockey, False],
        ),

        'city':'',
        'city_pk':-1,
        'hippodrome':'',
        'hippodrome_pk':-1,

        'title_race':'',
        'date':datetime.now().strftime("%Y-%m-%d"),
        'time_begin':datetime.now().strftime("%H:%M"),
        'time_end':datetime.now().strftime("%H:%M"),
        'distance':0,
        'summa':0,
        'org':'',

        'couples':[],
    }

    return render(request, 'mainapp/race_input_edit.html', context=context|custom_context)