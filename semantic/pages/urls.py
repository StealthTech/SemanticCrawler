from django.conf.urls import url

from . import views

app_name = 'pages'
urlpatterns = [
    url(r'^$', views.LandingView.as_view(), name='index'),
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^profile/(?P<nickname>[a-zA-Z0-9_]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^panel/$', views.PanelView.as_view(), name='panel'),
    url(r'^launch/$', views.LaunchView.as_view(), name='launch'),
    url(r'^results/(?P<pk>[0-9]+)/$', views.ScanResultView.as_view(), name='scan_results'),
]
