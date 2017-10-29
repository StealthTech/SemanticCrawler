from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.LandingView.as_view(), name='index'),
]
