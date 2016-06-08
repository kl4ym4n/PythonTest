from django.conf.urls import url

from . import views
from . import split_views


app_name = 'polls'

urlpatterns = [
    url(r'^register/$', views.register_user),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^addLink/$', split_views.add_link),
    url(r'^logout/$', views.logout_user),
    url(r'^publicLinks/$', split_views.display_public_links),
    url(r'^linkInfo/(\d{1,3})/$', split_views.display_link_info),
    url(r'^editLinkInfo/(\d{1,3})/$', split_views.display_edit_link_info),
    url(r'^allLinks/$', split_views.display_all_links),
    url(r'^deleteLink/(\d{1,3})/$', views.delete_link),
    url(r'^deleteUser/(\d{1,3})/$', views.delete_user),
    url(r'^userLinks/$', split_views.display_current_user_links),
    url(r'^usersList/$', split_views.display_user_list),
    url(r'^userProfile/$', split_views.display_user_profile),
    url(r'^editUserProfile/(\d{1,3})/$', split_views.display_edit_user_profile),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm),
    url(r'^$', views.index_view, name='index'),
    url(r'^403/$', views.display_403_page),
]
