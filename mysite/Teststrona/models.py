from django.db import models

# Create your models here.
class gigachad(models.Model):
    imie = models.CharField(max_length=50)

    def __str__(self):
        return self.imie