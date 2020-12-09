from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=50)
    card_image = models.ImageField(upload_to="cardimages", height_field=None, width_field=None, max_length=None)
    explanation = models.CharField(max_length=1000)
    inverted_explanation = models.CharField(max_length=1000)

   
    