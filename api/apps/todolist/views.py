from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import TodoListSerializer
from .services import TodoListService


class TodoListViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs: Any) -> None:
        self.__todo_list_service = TodoListService()

    @extend_schema(
        request=TodoListSerializer,
        responses={200: TodoListSerializer},
    )
    def create(self, request):
        todo_list = self.__todo_list_service.create(request.data)
        return Response(todo_list, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={200: TodoListSerializer},
    )
    def list(self, request):
        todo_lists = self.__todo_list_service.list()
        return Response(todo_lists, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: TodoListSerializer},
    )
    def retrieve(self, request, pk=None):
        todo_list = self.__todo_list_service.retrieve(pk)
        return Response(todo_list, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        self.__todo_list_service.destroy(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={202: TodoListSerializer},
        request=TodoListSerializer,
    )
    def update(self, request, pk=None):
        todo_list = self.__todo_list_service.update(pk, request.data)
        return Response(todo_list, status.HTTP_202_ACCEPTED)
