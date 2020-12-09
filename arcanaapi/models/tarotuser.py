from django.db import models
from django.contrib.auth.models import User


class Tarotuser(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    bio = models.CharField(max_length=500)
    profile_image = models.ImageField(upload_to="profileimages", height_field=None, width_field=None, max_length=None)
    astrology = models.ForeignKey("Sign", on_delete=models.CASCADE)
    card_of_day = models.models.ForeignKey("Card", on_delete=models.CASCADE)