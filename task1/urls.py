from django.urls import path
from .views import task1, task2, task3, evaluate,rectangle_view

urlpatterns = [
    path('task1/', task1, name='task1'),
    path('task2/', task2, name='task2'),
    path('task3/', task3, name='task3'),
    path('evaluate/', evaluate, name='evaluate'),
    path('rectangle/', rectangle_view, name='rectangle_view'),
]
