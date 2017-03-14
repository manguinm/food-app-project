from django.conf.urls import url

from . import views

app_name = 'foodapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /foodapp/5/
    url(r'^(?P<ingredient_id>[0-9]+)/$', views.ingredient_detail, name='ingredient_detail'),
    # ex: /foodapp/5/preferences-ingredient/
    url(r'^(?P<ingredient_id>[0-9]+)/preferences-ingredient/$', views.preferences_ingredient, name='preferences_ingredient'),
    # ex: /foodapp/5/rank-ingredient/
    url(r'^(?P<ingredient_id>[0-9]+)/rank-ingredient/$', views.rank_ingredient, name='rank_ingredient'),
    #  /foodapp/run-model/
    url(r'^run-model/$', views.run_model, name='run_model'),
    url(r'^model-results/$', views.model_results, name='model_results'),
    url(r'^rank-output/$', views.rank_output, name='rank_output'),
]