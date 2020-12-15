from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .card import Card
import random
from django.contrib.auth.signals import user_logged_in 
from django.dispatch import receiver



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

@receiver(user_logged_in, sender=User)
def my_handler(sender, instance, **kwargs):
    if instance.last_login.date() != timezone.now().date():
        #change card_of_day value on tarotuser
        tarotuser = Tarotuser.objects.get(user=instance)

        #use random integer to pick a random card
        cards = Card.objects.all()
        random_id = random.randint(1,22)
        card_of_day = cards[random_id]
        tarotuser.card_of_day = card_of_day

        #determine if card of day is inverted
        num = random.randint(1,4)

        if num == 1:
            tarotuser.card_of_day_inverted = True
        else:
            tarotuser.card_of_day_inverted = False
        tarotuser.save()

    instance.last_login = timezone.now()