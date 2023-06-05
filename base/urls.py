from django.urls import path
from .views import Tasklist, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('todo/', Tasklist.as_view(), name='tasklist'),
    path('todo/<int:pk>/', TaskDetail.as_view(), name='taskdetail'),
    path('create-task/', TaskCreate.as_view(), name='createtask'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='updatetask'),
    path('delete-task/<int:pk>/', TaskDelete.as_view(), name='deletetask'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='base/password-reset/html'), name='password_reset')
]