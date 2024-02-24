from typing import Any

from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import TodoListSerializer
from .services import AddTodoListService


class TodoListViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs: Any) -> None:
        self.__add_todo_list_service = AddTodoListService()

    def create(self, request):
        serializer = TodoListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo_list = self.__add_todo_list_service.handle(serializer)
        return Response(todo_list.data, status=status.HTTP_201_CREATED)
