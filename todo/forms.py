from django.forms import ModelForm # импортируем стандартные формы из джанго
from .models import Todo

# создаем нашу форму из модели в models.py для внесения записи
class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important'] # здесь пишем что будем отображать