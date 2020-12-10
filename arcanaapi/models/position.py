from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=50)
    layout = models.ForeignKey("Layout", on_delete=models.CASCADE)
    explanation = models.CharField(max_length=1000)