from django.db import models
import random


class Card(models.Model):
    name = models.CharField(max_length=50)
    card_image = models.ImageField(upload_to="cardimages", height_field=None, width_field=None, max_length=None)
    explanation = models.CharField(max_length=1000)
    inverted_explanation = models.CharField(max_length=1000)

    @property
    def inverted(self):
        """determines if the card is inverted or not

        Returns:
            boolean
        """
        num = random.randint(1,4)

        if num == 1:
            return True
        else:
            return False
        
   
    