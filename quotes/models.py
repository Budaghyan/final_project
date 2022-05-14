from django.db import models


class Quotes(models.Model):
    text = models.TextField(max_length=512)
    tag = models.ManyToManyField('tags.Tags')
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
