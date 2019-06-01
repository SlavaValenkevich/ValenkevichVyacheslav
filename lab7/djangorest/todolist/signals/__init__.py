from django.apps import AppConfig

class TodolistConfig(AppConfig):
    name = 'todolist'
    verbose_name = 'Todolist'

    def ready(self):
        import todolist.signals.handlers  # noqa