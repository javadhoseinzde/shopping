from django.db import models
from django.conf import settings
from shop.models import Item
from django.contrib.auth.models import User
from django.utils import timezone

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)