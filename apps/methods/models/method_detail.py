from django.db import models

class MethodDetail(models.Model):
    method = models.ForeignKey('MethodInitial', on_delete=models.CASCADE)
    details = models.TextField()

    def __str__(self):
        return f"Details for {self.method.name}"
