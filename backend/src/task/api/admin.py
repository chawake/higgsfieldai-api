from sqladmin import ModelView

from src.task.infrastructure.db.orm import TaskDB


class TaskAdmin(ModelView, model=TaskDB):
    name = "Task"
    column_list = "__all__"
