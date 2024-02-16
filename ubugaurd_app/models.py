# models.py
from django.db import models

class SearchEntry(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name
