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
        self.todo_list = TodoList.objects.create(
            title='valid_title', description='valid_description'
        )
        self.todo_list_service = TodoListService()

    @patch('apps.todolist.services.cache.delete')
    def test_create_service(self, mock_delete):
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

    def test_list_service(self):
        todo_lists = self.todo_list_service.list()
        self.assertEqual(todo_lists, [TodoListSerializer(self.todo_list).data])

    @patch('apps.todolist.services.cache.get')
    def test_should_call_get_cache_in_list_service(self, mock_get):
        self.todo_list_service.list()
        mock_get.assert_called_once()

    @patch('apps.todolist.services.cache.set')
    def test_should_call_set_cache_in_list_service(self, mock_set):
        todo_lists = self.todo_list_service.list()
        mock_set.assert_called_once()
        self.assertEqual(todo_lists, [TodoListSerializer(self.todo_list).data])

    def test_retrieve_service(self):
        todo_list = self.todo_list_service.retrieve(self.todo_list.pk)
        self.assertEqual(todo_list, TodoListSerializer(self.todo_list).data)

    @patch('apps.todolist.services.cache.get')
    def test_should_call_get_cache_in_retrieve_service(self, mock_get):
        self.todo_list_service.retrieve(self.todo_list.pk)
        mock_get.assert_called_once()

    @patch('apps.todolist.services.cache.set')
    def test_should_call_set_cache_in_retrieve_service(self, mock_set):
        todo_list = self.todo_list_service.retrieve(self.todo_list.pk)
        mock_set.assert_called_once()
        self.assertEqual(todo_list, TodoListSerializer(self.todo_list).data)

    def test_should_raise_404_when_id_not_found_in_retrieve_service(
        self,
    ):
        with self.assertRaises(Http404):
            self.todo_list.delete()
            self.todo_list_service.retrieve(self.todo_list.pk)

    @patch('apps.todolist.services.cache.delete')
    def test_destroy_service(self, mock_delete):
        self.todo_list_service.destroy(self.todo_list.pk)
        self.assertEqual(mock_delete.call_count, 2)
        self.assertTrue(
            mock_delete.call_args_list,
            [
                (('list-todolist')),
                ((f'retrieve-todolist-{self.todo_list.pk}')),
            ],
        )
        self.assertFalse(
            TodoList.objects.filter(id=self.todo_list.pk).exists()
        )

    def test_should_raise_404_when_id_not_found_in_destroy_service(
        self,
    ):
        with self.assertRaises(Http404):
            self.todo_list.delete()
            self.todo_list_service.destroy(self.todo_list.pk)
