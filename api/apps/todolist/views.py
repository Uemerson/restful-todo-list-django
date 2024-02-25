from typing import Any

from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import TodoListSerializer
from .services import TodoListService


class TodoListViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs: Any) -> None:
        self.__todo_list_service = TodoListService()

    def create(self, request):
        serializer = TodoListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        todo_list = self.__todo_list_service.create(serializer)
        return Response(todo_list.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        todo_lists = self.__todo_list_service.list()
        return Response(todo_lists, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        todo_list = self.__todo_list_service.retrieve(pk)
        return Response(todo_list, status=status.HTTP_200_OK)
