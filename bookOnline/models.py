from django.db import models

class LivreType(models.Model):
    genre = models.CharField(max_length=100)

    class Meta:
        db_table = 'LivreType'  # matches your existing MySQL table name

    def __str__(self):
        return self.genre


class LivreStatus(models.Model):
    status = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Livre Status"
        verbose_name_plural = "Livre Statuses"

    def __str__(self):
        return self.status


class Livre(models.Model):
    nom = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.ForeignKey(LivreType, on_delete=models.CASCADE)
    status = models.ForeignKey(LivreStatus, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Livre'  # matches your existing MySQL table name

    def __str__(self):
        return self.nom 