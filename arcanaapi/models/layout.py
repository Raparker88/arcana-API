from django.db import models


class Layout(models.Model):
    name = models.models.CharField(max_length=50)
    explanation = models.CharField(max_length=1000)