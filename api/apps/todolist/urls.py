from django.urls import path

from .views import TodoListViewSet

urlpatterns = [
    path(
        'todolist',
        TodoListViewSet.as_view({'post': 'create'}),
        name='create-todolist',
    )
]
