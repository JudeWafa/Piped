from django.db import models
from django.contrib.auth.models import User


# class User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # hash password when storing

#     def __str__(self):
#         return self.name


class Pipeline(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pipelines')

    def __str__(self):
        return f"{self.name} ({self.user.name})"


class Stage(models.Model):
    name = models.CharField(max_length=100)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')

    def __str__(self):
        return f"{self.name} ({self.pipeline.name})"


class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='items')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.title


class ItemHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='history')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='item_histories')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.title} → {self.stage.name} on {self.date_added.strftime('%Y-%m-%d %H:%M')}"
