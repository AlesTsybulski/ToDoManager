from django.db import models
from django.conf import settings

class Task(models.Model):

    srno = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    reminded = models.BooleanField(default=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({'done' if self.status else 'pending'})"