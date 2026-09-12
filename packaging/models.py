from django.db import models

class Box(models.Model):
    name = models.CharField(max_length=100, unique=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, help_text="Internal length in cm")
    width = models.DecimalField(max_digits=8, decimal_places=2, help_text="Internal width in cm")
    height = models.DecimalField(max_digits=8, decimal_places=2, help_text="Internal height in cm")
    max_weight = models.DecimalField(max_digits=8, decimal_places=2, help_text="Max weight capacity in kg")
    cost = models.DecimalField(max_digits=8, decimal_places=2, help_text="Box unit cost")

    class Meta:
        ordering = ['cost']

    @property
    def volume(self):
        return float(self.length * self.width * self.height)

    def __str__(self):
        return f"{self.name} ({self.length}x{self.width}x{self.height}cm - ₹{self.cost})"