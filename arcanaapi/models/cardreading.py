from django.db import models


class Cardreading(models.Model):
    
    card = models.ForeignKey("Card", on_delete=models.CASCADE)
    reading = models.ForeignKey("Reading", on_delete=models.CASCADE)
    position = models.ForeignKey("Position", on_delete=models.CASCADE)
    inverted = models.BooleanField()

    
