from django.db import models
from django.utils import timezone


class Subscription(models.Model):

    user = models.ForeignKey("Tarotuser", on_delete=models.CASCADE)
    follower = models.ForeignKey("Tarotuser", on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now())

   