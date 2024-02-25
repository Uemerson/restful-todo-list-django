from typing import Any

from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import TodoListSerializer
from .services import AddTodoListService, ListTodoListService


class TodoListViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs: Any) -> None:
        self.__add_todo_list_service = AddTodoListService()
        self.__list_todo_list_service = ListTodoListService()

    def create(self, request):
        serializer = TodoListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo_list = self.__add_todo_list_service.handle(serializer)
        return Response(todo_list.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        todo_list = self.__list_todo_list_service.handle()
        return Response(todo_list, status=status.HTTP_200_OK)
