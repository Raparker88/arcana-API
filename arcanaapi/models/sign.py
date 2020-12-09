from django.db import models


class Sign(models.Model):
    name = models.models.CharField(max_length=50)
    