from django.shortcuts import render, redirect, get_object_or_404 # redirect для перенаправления по страницам
# импортируем из библиотеки готовую форму авторизации
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# вернуть модель пользователя
from django.contrib.auth.models import User
# импортируем ошибку возникающую при повторной регистрации пользователя
from django.db import IntegrityError
# чтобы пользователь не мог попасть на админскую панель, а попадал на страницу своего аккаунта
from django.contrib.auth import login, logout, authenticate
# импорт нашей созданной формы
from .forms import TodoForm
# импортируем записи пользователя
from .models import Todo
from django.utils import timezone
# чтобы при прямом переходе из адресной строки показывало, что только зарегестрированные пользователи могут попадать на внутренние страницы
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def signupuser(request):
    if request.method == 'GET': # если пользователь хочет получить данные с сайта, то возвращаем ему форму. Когда в адресной строке браузера вводят данные, то всегда работает метод GET. Метод POST работает только в специальных формах на странице
        return render(request, 'signupuser.html', {'form':UserCreationForm()})
    else:
        # создать пользователя
        if request.POST['password1'] == request.POST['password2']: # если пароли совпадают, то можно создать пользователя
            try: # блок для обработки ошибки если пользователь уже существует
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1']) # передаем данные для создания пользователя из метода POST. Названия "username" и "password" можно посмотреть на странице браузера нажав правой кнопкой мыши на странице и выбрать "посмотреть код страницы". Там найти нужные поля и посмотреть их "name". И присвоим переменной "user"
                user.save() # команда для сохранения пользователя
                login(request, user) # это, чтобы перенаправить пользователя на свою страницу
                return redirect('currenttodos')
            except IntegrityError: # исключение IntegrityError можно увидеть если без блока обработки ошибки зарегать повторно одинакового пользователя
                return render(request, 'signupuser.html', {'form': UserCreationForm(), 'error': 'Пользователь с таким именем уже существует. Выберите другое имя!'})
        else:
            # ошибка. пароли не совпадают
            return render(request, 'signupuser.html', {'form':UserCreationForm(), 'error':'Пароли не совпадают! Повторите ввод.'}) # выдаем снова форму ввода пароля и сообщаем об ошибке

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form':AuthenticationForm()}) # jnrhsdftv cnhfybwe gjkmpj
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password']) # передаем данные для авторизации пользователя из метода POST. Названия "username" и "password" можно посмотреть на странице браузера нажав правой кнопкой мыши на странице и выбрать "посмотреть код страницы". Там найти нужные поля и посмотреть их "name". И присвоим переменной "user"
        if user is None: # если пользователя не существует перенаправляем его на страницу авторизации и выдаем ошибку
            return render(request, 'loginuser.html', {'form': AuthenticationForm(), 'error':'Проверьте корректность введенных данных'})
        else: # если пользователь существует
            login(request, user)  # это, чтобы перенаправить пользователя на свою страницу
            return redirect('currenttodos')

@login_required # только зарегестрированные пользователи имееют доступ сюда
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        # возвращаемся на домошнюю страницу
        return redirect('home')

@login_required # только зарегестрированные пользователи имееют доступ сюда
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST) # загружаем полученную инфу от пользователя в нашу форму
            newtodo = form.save(commit=False) # Помещаем это в переменную, чтобы можно было потом связать с конкретным пользователем
            newtodo.user = request.user # поле user заполняется текущим пользователем из request.user
            newtodo.save() # сохраняем запись в БД
            return redirect('currenttodos')
        except ValueError:
            return redirect(request, 'currenttodo.html', {'form':TodoForm(), 'error':'Переданы неверные данные. Попробуйте еще раз'})

@login_required # только зарегестрированные пользователи имееют доступ сюда
def currenttodos(request): # функция перенаправляет пользователя на страницу пользователя
    # todos = Todо.objects.all() # достаем все записи для пользователя. Так достанутся все записи в БД
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True) # применяем фильтр чтобы записи показывались конкретного пользователя. datecompleted__isnull проверка на завершение задачи, если True (незавершена), то показываем ее. В фильтре можно писать разные условия через запятую
    return render(request, 'currenttodos.html', {'todos':todos})

@login_required # только зарегестрированные пользователи имееют доступ сюда
def completedtodos(request): # функция перенаправляет пользователя на страницу завершенных задач
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') # применяем фильтр чтобы записи показывались конкретного пользователя. datecompleted__isnull проверка на завершение задачи, если False (завершена), то показываем ее. В фильтре можно писать разные условия через запятую. Order_by - сортировка знак минус означает в обратном порядке
    return render(request, 'completedtodos.html', {'todos':todos})

@login_required # только зарегестрированные пользователи имееют доступ сюда
def viewtodo(request, todo_pk): # добавили ключ записи
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) # если объект есть показываем по ключу pk=todo_pk, иначе ошибка 404. user=request.user - чтобы пользователь не мог просматривать чужие записи введя в адресной строке прямой путь к записи
    if request.method == 'GET':# сохранение отредактированной задачи в БД
        form = TodoForm(instance=todo)  # для работы с созданной записью
        return render(request, 'viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo) # чтобы не было конфликта какую форму мы используем (для создания объекта или редактирования) вносим уточнение instance=todо
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'viewtodo.html', {'todo': todo, 'form': form, 'error':'Bad info'})

@login_required # только зарегестрированные пользователи имееют доступ сюда
def completetodo(request, todo_pk): # завершать задачу сможет только тот пользователь который ее создал
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now() # признак, что задача завершена, если поле datecompleted не пустое. При нажатии кнопки Выполнено сюда впишется текущая дата
        todo.save()
        return redirect('currenttodos')

@login_required # только зарегестрированные пользователи имееют доступ сюда
def deletetodo(request, todo_pk): # удалить задачу сможет только тот пользователь который ее создал
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')