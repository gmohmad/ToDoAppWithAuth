from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['is_complete', '-created']

    def __str__(self):
        return self.name
