from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .models import TodoList
from .serializers import TodoListSerializer


class TodoListService:
    def create(self, todo_list: TodoListSerializer):
        todo_list.save()
        for key in ['list-todolist']:
            cache.delete(key)
        return todo_list

    def list(self):
        todo_lists = cache.get('list-todolist')
        if not todo_lists:
            todo_lists = TodoList.objects.all()
            serializer = TodoListSerializer(todo_lists, many=True)
            cache.set('list-todolist', serializer.data, timeout=None)
            return serializer.data
        return todo_lists

    def retrieve(self, pk: str):
        todo_list = cache.get(f'retrieve-todolist-{pk}')
        if not todo_list:
            todo_list = get_object_or_404(TodoList, pk=pk)
            serializer = TodoListSerializer(todo_list)
            cache.set(f'retrieve-todolist-{pk}', serializer.data, timeout=None)
            return serializer.data
        return todo_list

    def destroy(self, pk: str):
        todo_list = get_object_or_404(TodoList, pk=pk)
        todo_list.delete()
        cache.delete(f'retrieve-todolist-{pk}')
        cache.delete('list-todolist')

    def update(self, pk: str, data: dict):
        todo_list = get_object_or_404(TodoList, pk=pk)
        serializer = TodoListSerializer(
            instance=todo_list, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'retrieve-todolist-{pk}')
        cache.delete('list-todolist')
        return serializer.data
