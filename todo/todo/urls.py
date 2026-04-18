
from django.contrib import admin
from django.urls import path

from users import views as user_views
from tasks import views as task_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Маршруты пользователей
    path('signup/', user_views.signup, name='signup'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.signout, name='logout'),
    
    # Маршруты задач
    path('', task_views.home, name='home'),
    path('todopage/', task_views.todo, name='todo'),
    path('delete_todo/<int:srno>/', task_views.delete_todo, name='delete_todo'),
    path('edit_todo/<int:srno>/', task_views.edit_todo, name='edit_todo'),
    path('toggle_todo/<int:srno>/', task_views.toggle_todo, name='toggle_todo'),
]