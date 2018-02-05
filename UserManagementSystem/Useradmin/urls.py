from django.conf.urls import url
from Useradmin import views

urlpatterns = [
    url(r'^login.html$', views.login),
    url(r'^check_code/', views.check_code),
    url(r'^register/', views.register),
    url(r'^avator_input/', views.avator_input),
    
    url(r'^usersinfo/(\d+)/', views.users_infos),
    url(r'^usersinfo/', views.users_info),
    url(r'^usersinfo_json/', views.Usersinfo.as_view()),
    
    
    url(r'^groupinfo/(\d+)/', views.groups_infos),
    url(r'^groupinfo/', views.groups_info),
    url(r'^groupinfo_json/', views.Groupinfo.as_view()),
]