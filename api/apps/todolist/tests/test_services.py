from unittest.mock import patch

from django.test import TestCase, override_settings

from ..models import TodoList
from ..serializers import TodoListSerializer
from ..services import AddTodoListService, ListTodoListService


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

    @patch('apps.todolist.services.cache.delete')
    def test_add_todo_list_service(self, mock_delete):
        todo_list_data = {
            'title': 'valid_title',
            'description': 'valid_description',
        }
        serializer = TodoListSerializer(data=todo_list_data)
        self.assertTrue(serializer.is_valid())
        service = AddTodoListService()
        saved_todo_list = service.handle(serializer)
        mock_delete.assert_called_once()
        self.assertTrue(
            TodoList.objects.filter(id=saved_todo_list.data['id']).exists()
        )
        self.assertEqual(saved_todo_list.data, serializer.data)

    def test_list_todo_list_service(self):
        service = ListTodoListService()
        todo_lists = service.handle()
        self.assertEqual(todo_lists, [TodoListSerializer(self.todolist).data])

    @patch('apps.todolist.services.cache.get')
    def test_should_call_get_cache_in_list_todo_list_service(self, mock_get):
        service = ListTodoListService()
        service.handle()
        mock_get.assert_called_once()

    @patch('apps.todolist.services.cache.set')
    def test_should_call_set_cache_in_list_todo_list_service(self, mock_set):
        service = ListTodoListService()
        todo_lists = service.handle()
        mock_set.assert_called_once()
        self.assertEqual(todo_lists, [TodoListSerializer(self.todolist).data])
