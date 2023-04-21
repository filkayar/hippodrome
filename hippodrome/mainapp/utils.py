visitors_menu = [
    {'title': "Список лошадей", 'url_name': 'list_horses'},
    {'title': "Список жокеев", 'url_name': 'list_jockey'},
]

admin_menu = [
    {'title': "Список лошадей", 'url_name': 'list_horses'},
    {'title': "Список жокеев", 'url_name': 'list_jockey'},
    {'title': "Список пользователей", 'url_name': 'list_users'},
    {'title': "Список печати", 'url_name': 'list_print'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
