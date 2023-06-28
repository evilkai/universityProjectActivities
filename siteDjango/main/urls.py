from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('logout_views', views.logout_view, name='logout'),
    path('admin/', views.apanel, name='apanel'),
    path("register", views.register, name="register"),



    path('staff/tasks', views.tasks, name='tasks'),
    path('staff/requests', views.requests, name='requests'),
    path('staff/archive', views.archive, name='archive'),
    path('staff/tasks/<int:pk_page>/', views.taskpage, name='taskpage'),
    path('staff/requests/<int:pk_page>/', views.requestpage, name='requestpage'),



    #### CLIENT ####
    path('client/cards', views.cards, name='cards'),
    path('client/newcard', views.newcard, name='newcard'),
    path('client/credit', views.credit, name='credit'),
    path('client/offers', views.offers, name='offers'),
    path('client/moneytransfer', views.moneytransfer, name='moneytransfer'),
    path('client/creditrequest', views.creditrequest, name='creditrequest'),
] 
 