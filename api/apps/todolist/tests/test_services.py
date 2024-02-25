from unittest.mock import patch

from django.http import Http404
from django.test import TestCase, override_settings

from ..models import TodoList
from ..serializers import TodoListSerializer
from ..services import TodoListService


@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
)
class TodoListServicesTestCase(TestCase):
    def setUp(self):
        self.todolist = TodoList.objects.create(
            title='valid_title', description='valid_description'
        )
        self.todo_list_service = TodoListService()

    @patch('apps.todolist.services.cache.delete')
    def test_create_todo_list_service(self, mock_delete):
        todo_list_data = {
            'title': 'valid_title',
            'description': 'valid_description',
        }
        serializer = TodoListSerializer(data=todo_list_data)
        self.assertTrue(serializer.is_valid())
        todo_list = self.todo_list_service.create(serializer)
        mock_delete.assert_called_once()
        self.assertTrue(
            TodoList.objects.filter(id=todo_list.data['id']).exists()
        )
        self.assertEqual(todo_list.data, serializer.data)

    def test_list_todo_list_service(self):
        todo_lists = self.todo_list_service.list()
        self.assertEqual(todo_lists, [TodoListSerializer(self.todolist).data])

    @patch('apps.todolist.services.cache.get')
    def test_should_call_get_cache_in_list_todo_list_service(self, mock_get):
        self.todo_list_service.list()
        mock_get.assert_called_once()

    @patch('apps.todolist.services.cache.set')
    def test_should_call_set_cache_in_list_todo_list_service(self, mock_set):
        todo_lists = self.todo_list_service.list()
        mock_set.assert_called_once()
        self.assertEqual(todo_lists, [TodoListSerializer(self.todolist).data])

    def test_retrieve_todo_list_service(self):
        todo_list = self.todo_list_service.retrieve(self.todolist.pk)
        self.assertEqual(todo_list, TodoListSerializer(self.todolist).data)

    @patch('apps.todolist.services.cache.get')
    def test_should_call_get_cache_in_retrieve_todo_list_service(
        self, mock_get
    ):
        self.todo_list_service.retrieve(self.todolist.pk)
        mock_get.assert_called_once()

    @patch('apps.todolist.services.cache.set')
    def test_should_call_set_cache_in_retrieve_todo_list_service(
        self, mock_set
    ):
        todo_list = self.todo_list_service.retrieve(self.todolist.pk)
        mock_set.assert_called_once()
        self.assertEqual(todo_list, TodoListSerializer(self.todolist).data)

    def test_should_raise_404_when_id_not_found_in_retrieve_todo_list_service(
        self,
    ):
        with self.assertRaises(Http404):
            self.todolist.delete()
            self.todo_list_service.retrieve(self.todolist.pk)

    @patch('apps.todolist.services.cache.delete')
    def test_destroy_todo_list_service(self, mock_delete):
        self.todo_list_service.destroy(self.todolist.pk)
        mock_delete.assert_called_once()
        self.assertFalse(TodoList.objects.filter(id=self.todolist.pk).exists())

    def test_should_raise_404_when_id_not_found_in_destroy_todo_list_service(
        self,
    ):
        with self.assertRaises(Http404):
            self.todolist.delete()
            self.todo_list_service.destroy(self.todolist.pk)
