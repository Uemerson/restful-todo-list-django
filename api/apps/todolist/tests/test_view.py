import json

from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status

from ..models import TodoList
from ..serializers import TodoListSerializer


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
)
class TodoListViewsTestCase(TestCase):
    def setUp(self):
        self.todolist = TodoList.objects.create(
            title='valid_title', description='valid_description'
        )

    def test_create_todo_list_viewset(self):
        data = {'title': 'valid_title', 'description': 'valid_description'}
        count_todo_list = TodoList.objects.count()
        response = self.client.post(reverse('todolist'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TodoList.objects.count(), count_todo_list + 1)

    def test_list_todo_list_viewset(self):
        response = self.client.get(reverse('todolist'))
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content, [TodoListSerializer(self.todolist).data])
