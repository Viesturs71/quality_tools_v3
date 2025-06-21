# methods/models/akk_registrs.py
from django.db import models


class AkkRegistrs(models.Model):
    pakalpojuma_sniedzejs = models.CharField(max_length=255, verbose_name="Pakalpojuma sniedzējs")
    laboratorija = models.CharField(max_length=255, verbose_name="Laboratorija")
    kods = models.CharField(max_length=100, verbose_name="Kods")
    izmeklejamais_materials = models.CharField(max_length=255, verbose_name="Izmeklējamais materiāls")
    tehnologija_izmeklejums = models.CharField(max_length=255, verbose_name="Tehnoloģija / izmeklējums")
    skaits = models.PositiveIntegerField(verbose_name="Skaits")
    cena = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena (€)")
    testa_summa = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Testa summa (€)")

    class Meta:
        verbose_name = "Akk reģistrs"
        verbose_name_plural = "Akk reģistri"

    def __str__(self):
        return f"{self.pakalpojuma_sniedzejs} - {self.laboratorija} ({self.kods})"
