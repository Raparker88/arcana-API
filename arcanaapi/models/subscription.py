from django.db import models
from django.utils import timezone


class Subscription(models.Model):

    user = models.ForeignKey("Tarotuser", on_delete=models.CASCADE, related_name='subscribers')
    follower = models.ForeignKey("Tarotuser", on_delete=models.CASCADE, related_name='subscriptions')
    date_created = models.DateTimeField(default=timezone.now)

    

   