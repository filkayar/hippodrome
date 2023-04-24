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
                obj['records'].append(dict(pk=o.id, photo=o.photo.url, value=o.__str__()))

        list_v.append(obj)

    return list_v

def get_default_context(request):
    return {
        'side_menu': get_side_menu(request),
        'punkt_selected': -1,
        'is_login': request.user.is_authenticated,
        'is_admin': request.user.is_superuser,
        'is_self_or_admin': request.user.is_superuser or request.user.id == rec.id,
        'list_v': [],
        'photo': '',
    }