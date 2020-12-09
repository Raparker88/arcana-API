from django.db import models


class Card(models.Model):
    name = models.models.CharField(max_length=50)
    card_image = models.models.ImageField(upload_to="cardimages", height_field=None, width_field=None, max_length=None)
    explanation = models.models.CharField(max_length=1000)
    inverted_explanation = models.models.CharField(max_length=1000)

   
    