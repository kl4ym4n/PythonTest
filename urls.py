from django.conf.urls import url

from . import views

app_name = 'polls'

urlpatterns = [
    url(r'^register/$', views.register_user),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^addLink/$', views.add_link),
    url(r'^PublicLinks/$', views.display_public_links),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^time/$', views.current_datetime),
    url(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
]