from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.home, name='blog-home'),
    path('pulpit/', views.mystats, name='blog-desktop'),
    path('polaczenia/', views.phonecalls, name='blog-phonecalls'), 
    path('polaczenia/dodaj/', views.add_phonecall, name='add-phonecall'),
    path('spotkania/', views.meetings, name='blog-meetings'),
    path('spotkania/dodaj/', views.add_meeting, name='add-meeting'),
    path('kalendarz/', views.calendar, name='blog-calendar'),
    path('login/', views.login_request, name='blog-login'),
    path('logout/', views.logout_request, name='blog-logout'),
    url(r'^klient/$', views.client_detail, name='blog-client'),
    url(r'^klient/(?P<id>\d+)/$', views.client_detail, name='blog-client-search'),
    url(r'^search/$', views.search, name='blog-search'),
]