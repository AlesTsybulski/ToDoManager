from django.contrib import admin
from tasks.models import Task
from users.models import User


admin.site.register(Task)
admin.site.register(User)
