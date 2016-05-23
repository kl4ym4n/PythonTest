from django.conf.urls import url

from . import views

app_name = 'polls'

urlpatterns = [
    url(r'^register/$', views.register_user),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^addLink/$', views.add_link),
    url(r'^logout/$', views.logout_user),
    url(r'^publicLinks/$', views.display_public_links),
    url(r'^allLinks/$', views.display_all_links),
    url(r'^userLinks/$', views.display_current_user_links),
    url(r'^usersList/$', views.display_user_list),
    url(r'^userProfile/$', views.display_user_profile),
    url(r'^editUserProfile/$', views.display_edit_user_profile),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^time/$', views.current_datetime),
    url(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
]