from django.db import models
from django.utils import timezone


class Comment(models.Model):

    tarotuser = models.ForeignKey("Tarotuser", on_delete=models.CASCADE, related_name="tarotuser")
    date_created = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=2000)
    reading = models.ForeignKey("Reading", on_delete=models.CASCADE, related_name="comments")
    