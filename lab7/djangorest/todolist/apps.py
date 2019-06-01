from django.apps import AppConfig


class TodolistConfig(AppConfig):
    name = 'todolist'
    verbose_name = 'Todolist'
    def ready(self):
        print('hello,im ready')
        import todolist.signals.headers
