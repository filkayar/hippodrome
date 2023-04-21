from django.urls import path
from .views import *


urlpatterns = [
    path('repports/', RepportsList.as_view(), name='repports_list'),

    path('', RacesList.as_view(), name='races_list'),
    path('race/<int:record>/', RaceId.as_view(), name='race_id'),
    path('race/edit/<int:record>/', RaceEdit.as_view(), name='race_edit'),
    path('race/edit/new', RaceNew.as_view(), name='race_new'),

    path('horses', HorsesList.as_view(), name='horses_list'),
    path('horse/<int:record>/', HorseId.as_view(), name='horse_id'),
    path('horse/edit/<int:record>', HorseEdit.as_view(), name='horse_edit'),
    path('horse/edit/new', HorseNew.as_view(), name='horse_new'),

    path('jockeys', JockeysList.as_view(), name='jockeys_list'),
    path('jockey/<int:record>/', JockeyId.as_view(), name='jockey_id'),
    path('jockey/edit/<int:record>', JockeyEdit.as_view(), name='jockey_edit'),
    path('jockey/edit/new', JockeyNew.as_view(), name='jockey_new'),

    path('owners', OwnersList.as_view(), name='owners_list'),
    path('owner/<int:record>/', OwnerId.as_view(), name='owner_id'),
    path('owner/edit/<int:record>', OwnerEdit.as_view(), name='owner_edit'),
    path('owner/edit/new', OwnerNew.as_view(), name='owner_new'),

]