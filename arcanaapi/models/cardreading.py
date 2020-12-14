from django.db import models


class Cardreading(models.Model):
    
    card = models.ForeignKey("Card", on_delete=models.CASCADE, related_name="cardreadings")
    reading = models.ForeignKey("Reading", on_delete=models.CASCADE, related_name="cardreadings")
    position = models.ForeignKey("Position", on_delete=models.CASCADE)
    inverted = models.BooleanField()

    
