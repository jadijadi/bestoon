from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/expense/$', views.submit_expense, name='submit_expense'),
    url(r'^submit/income/$', views.submit_income, name='submit_income'),
]
