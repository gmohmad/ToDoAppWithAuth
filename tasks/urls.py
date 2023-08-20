from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', TasksList.as_view(), name='home'),

    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

    path('task/<str:pk>/', TaskDetail.as_view(), name='task'),
    path('task-update/<str:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-delete/<str:pk>/', TaskDelete.as_view(), name='task-delete'),

]
