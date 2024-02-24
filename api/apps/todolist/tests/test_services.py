from django.test import TestCase

from ..models import TodoList
from ..serializers import TodoListSerializer
from ..services import AddTodoListService


class TodoListServicesTestCase(TestCase):
    def test_add_todo_list_service(self):
        todo_list_data = {
            'title': 'valid_title',
            'description': 'valid_description',
        }
        serializer = TodoListSerializer(data=todo_list_data)
        self.assertTrue(serializer.is_valid())
        service = AddTodoListService()
        saved_todo_list = service.handle(serializer)

        self.assertTrue(TodoList.objects.filter(title='valid_title').exists())
        self.assertEqual(saved_todo_list.data, serializer.data)
