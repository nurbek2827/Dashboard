from django.db import models


class Ishchi(models.Model):
    name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    age = models.IntegerField("Yoshi")
    salary = models.CharField(max_length=128)
    position = models.CharField(max_length=128)

    def __str__(self):
        return self.name