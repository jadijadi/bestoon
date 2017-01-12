from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/expense/?$', views.submit_expense, name='submit_expense'),
    url(r'^submit/income/?$', views.submit_income, name='submit_income'),
    url(r'^q/expencestat/?$', views.expencestat, name='expencestat'),
    url(r'^q/incomestat/?$', views.expencestat, name='incomestat'),
    url(r'^q/generalstat/?$', views.generalstat, name='generalstat'),
    url(r'^accounts/register/?$', views.register, name='register'),
    url(r'^accounts/whoami/?$', views.whoami, name='whoami'),
    url(r'^accounts/login/?$', views.login, name='login'),
    url(r'^$', views.index, name='index'),
]