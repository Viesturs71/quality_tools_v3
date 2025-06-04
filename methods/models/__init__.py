from django.db import models


class MetozuRegistrs(models.Model):
    nosaukums = models.CharField(max_length=255)
    apraksts = models.TextField()

    def __str__(self):
        return self.nosaukums
