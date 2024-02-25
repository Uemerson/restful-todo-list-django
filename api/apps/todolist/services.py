from django.core.cache import cache

from .models import TodoList
from .serializers import TodoListSerializer


class TodoListService:
    def create(self, todo_list: TodoListSerializer) -> TodoListSerializer:
        todo_list.save()
        for key in ['list-todolist']:
            cache.delete(key)
        return todo_list

    def list(self) -> list[dict]:
        todo_lists = cache.get('list-todolist')
        if not todo_lists:
            todo_lists = TodoList.objects.all()
            serializer = TodoListSerializer(todo_lists, many=True)
            cache.set('list-todolist', serializer.data, timeout=None)
            return serializer.data
        return todo_lists
