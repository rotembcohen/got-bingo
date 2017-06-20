from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Square(models.Model):
    text = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text

class Board(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_bingoed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.username + "'s board"

class BoardCell(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    square = models.ForeignKey(Square, on_delete=models.CASCADE)
    x_val = models.PositiveSmallIntegerField()
    y_val = models.PositiveSmallIntegerField()
    marked = models.BooleanField(default=False)
    wildcard = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)
