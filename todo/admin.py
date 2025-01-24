from django.contrib import admin
from .models import Todo


class TodoAdmin(admin.ModelAdmin):# для отображения даты created в models.py которая является не редактируемой
    readonly_fields = ('created',)

admin.site.register(Todo, TodoAdmin) # добавляем в админскую панель модель Todos и класс выше
