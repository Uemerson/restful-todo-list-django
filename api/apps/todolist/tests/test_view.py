from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ..models import TodoList


class TodoListViewsTestCase(TestCase):
    def test_create_todo_list_viewset(self):
        data = {'title': 'valid_title', 'description': 'valid_description'}
        count_todo_list = TodoList.objects.count()
        response = self.client.post(reverse('create-todolist'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoList.objects.count(), count_todo_list + 1)
