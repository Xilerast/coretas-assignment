from django.urls import path
from api.views import (task_view, user_view, misc)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


# This is the list of our routes
urlpatterns = [
    path('', misc.default, name='default'),
    path('csrf/', misc.get_token, name="csrf"),
    path('tasks/', task_view.getTasks, name='tasks'),
    path('tasks/<str:pk>/', task_view.getTask, name='task'),
    path('tasks/create', task_view.createTask, name='createTask'),
    path('tasks/edit', task_view.updateTask, name="updateTask"),
    path('tasks/complete', task_view.completeTask, name="completeTask"),
    path('tasks/delete', task_view.deleteTask, name="deleteTask"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', user_view.registerUser, name="registerUser")
]

