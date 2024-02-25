from django.urls import path

from .views import TodoListViewSet

urlpatterns = [
    path(
        'todolist',
        TodoListViewSet.as_view({'post': 'create', 'get': 'list'}),
        name='todolist',
    ),
]
