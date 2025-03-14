from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Nombre único

    def __str__(self):
        return self.name
