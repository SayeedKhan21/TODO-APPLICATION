from django.shortcuts import render
from django.http import HttpResponse
from django.urls import path 
from .views import * 
urlpatterns =[
    path('' , TaskList.as_view() , name = 'tasks') ,
    path('login/' , CustomLoginView.as_view() , name = 'login') ,
    path('logout/' , CustomLogoutView.as_view() , name = 'logout') ,
    path('register/' , RegisterPage.as_view() , name = 'register') ,
    path('task-create' , TaskCreate.as_view() , name = 'create-task') ,
    path('task-update/<int:pk>/' , TaskUpdate.as_view() , name = 'update-task') ,
    path('task-delete/<int:pk>/' , TaskDelete.as_view() , name = 'delete-task') ,
    path('task/<int:pk>/' , TaskDetail.as_view() , name = 'task') ,
]