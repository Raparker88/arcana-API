from django.db import models
from django.contrib.auth.models import User



class Tarotuser(models.Model):

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING,)
    bio = models.CharField(max_length=500)
    profile_image = models.ImageField(upload_to="profileimages", height_field=None, width_field=None, max_length=None)
    astrology = models.ForeignKey("Sign", on_delete=models.CASCADE)
    card_of_day = models.ForeignKey("Card", on_delete=models.CASCADE, related_name = "card_of_day")
    card_of_day_inverted = models.BooleanField()


    """This makes the username property accessible directly from the User table"""
    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return (f'{self.user.first_name} {self.user.last_name}')

    @property
    def subscribed(self):
        return self.__subscribed

    @subscribed.setter
    def subscribed(self, value):
        self.__subscribed = value
        



    