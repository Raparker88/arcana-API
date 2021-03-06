from django.db import models
from django.utils import timezone


class Reading(models.Model):

    tarotuser = models.ForeignKey("Tarotuser", on_delete=models.CASCADE, related_name="readings")
    date_created = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50)
    layout = models.ForeignKey("Layout", on_delete=models.CASCADE)
    shared = models.BooleanField(default=False)
    notes = models.CharField(max_length=2000)

    @property
    def comment_count(self):
        comments = self.comments.all()
        return len(comments)
