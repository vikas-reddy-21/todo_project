from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('complete/<int:todo_id>/', views.toggle_complete, name='toggle_complete'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]
