from django.urls import path
from api.views import (task_view, user_view, misc)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


# This is the list of our routes
urlpatterns = [
    path('', misc.default, name='default'),
    path('csrf/', misc.csrf, name="csrf"),
    path('tasks/', task_view.getTasks, name='tasks'),
    path('tasks/<str:pkey>/', task_view.getTask, name='task'),
    path('tasks/create', task_view.createTask, name='createTask'),
    path('tasks/edit/<str:pkey>/', task_view.updateTask, name="updateTask"),
    path('tasks/complete/<str:pkey>/', task_view.completeTask, name="completeTask"),
    path('tasks/delete/<str:pkey>/', task_view.deleteTask, name="deleteTask"),
    path('login/', user_view.loginUser, name='login'),
    path('register/', user_view.registerUser, name="registerUser")
]

