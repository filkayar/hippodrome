from django.urls import path
from .views import *

urlpatterns = [
    path('races/edit/new', RaceNew, name='race_new'),
    path('races/edit/<int:record>', RaceEdit, name='race_edit'),
    path('races/<int:record>', RaceId, name='race_id'),

    path('horses/edit/<int:record>', HorseEdit, name='horse_edit'),
    path('horses/<int:record>', HorseId, name='horse_id'),
    path('horses', HorsesList, name='horses_list'),

    path('jockeys/edit/<int:record>', JockeyEdit, name='jockey_edit'),
    path('jockeys/<int:record>', JockeyId, name='jockey_id'),
    path('jockeys', JockeysList, name='jockeys_list'),

    path('owners/edit/<int:record>', OwnerEdit, name='owner_edit'),
    path('owners/<int:record>', OwnerId, name='owner_id'),
    path('owners', OwnersList, name='owners_list'),

    path('', RacesList, name='races_list'),
    path('reports', RepportsList, name='reports_list'),
    path('report/<str:report_name>', Render_pdf_view, name='report_print'),

    path('error_access', ErrorAccess, name='err_access'),
]