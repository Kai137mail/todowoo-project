from django.db import models
# чтобы была привязка модели к пользователю. Чтобы можно было связывать модели между собой
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True) # blank=True значит поле необязательно к заполнению
    created = models.DateTimeField(auto_now_add=True) # в скобках автозаполнение даты. Его нельзя потом менять
    datecompleted = models.DateTimeField(null=True, blank=True) # по умолчанию пустое, т.к. поле с типом DateTimeField обязательное для заполнения
    important = models.BooleanField(default=False) # default=False значит поле необязательно к заполнению
    user = models.ForeignKey(User, on_delete=models.CASCADE) # этот ключ определяет созданного пользователя с записью в БД

    def __str__(self): # чтобы в админской панели перечень задач назывался по имени задачи
        return self.title
# не забываем делать миграцию после изменения модели
# python3 manage.py makemigrations
# python3 manage.py migrate