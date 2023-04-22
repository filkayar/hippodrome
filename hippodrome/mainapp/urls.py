from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('races/edit/new', RaceNew, name='race_new'),
    path('races/edit/<int:record>/', RaceEdit, name='race_edit'),
    path('races/<int:record>/', RaceId, name='race_id'),

    path('horses/edit/new', HorseNew, name='horse_new'),
    path('horses/edit/<int:record>', HorseEdit, name='horse_edit'),
    path('horses/<int:record>/', HorseId, name='horse_id'),
    path('horses/', HorsesList, name='horses_list'),

    path('jockeys/edit/new', JockeyNew, name='jockey_new'),
    path('jockeys/edit/<int:record>', JockeyEdit, name='jockey_edit'),
    path('jockeys/<int:record>/', JockeyId, name='jockey_id'),
    path('jockeys/', JockeysList, name='jockeys_list'),

    path('owners/edit/new', OwnerNew, name='owner_new'),
    path('owners/edit/<int:record>', OwnerEdit, name='owner_edit'),
    path('owners/<int:record>/', OwnerId, name='owner_id'),
    path('owners/', OwnersList, name='owners_list'),

    path('', RacesList, name='races_list'),
    path('login/', LoginUser, name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('reports/', RepportsList, name='reports_list'),
]