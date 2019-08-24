from django.urls import path
from . import views

app_name = 'webapp'


urlpatterns = [
    path('', views.index, name="homepage"),
    path('login', views.login, name="login"),
    path('stats', views.stats, name='stats'),
    path('organization', views.organization, name="organization"),
    path('organization/statistics', views.org_stats, name="organization_stats"),
    path('homedata', views.house_information, name="house"),
    path('recomment', views.recommend, name='recommend'),
    path('do', views.do_stuff, name='do'),
    path('simulation', views.simulation, name='simulation'),
    path('sim', views.index_sim, name='index_sim'),
    path('sample', views.sample, name='sample'),
    path('chaar', views.index_last_hope, name='chaar')

]