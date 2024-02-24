from .serializers import TodoListSerializer


class AddTodoListService:
    def handle(self, todo_list: TodoListSerializer) -> TodoListSerializer:
        todo_list.save()
        return todo_list
