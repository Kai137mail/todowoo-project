"""
URL configuration for todowoo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# импортируем вьюшки, на которые ссылаемся
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Авторизация на сайте
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    # Для записей todos
    path('', views.home, name='home'),
    path('current/', views.currenttodos, name='currenttodos'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('create/', views.createtodo, name='createtodo'),
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'), # страница задачи со ссылкой на primarykey в БД
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'), # страница отметки о выполнении задачи
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'), #
]
