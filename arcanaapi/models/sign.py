from django.db import models


class Sign(models.Model):
    name = models.CharField(max_length=50)
    