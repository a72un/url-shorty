from django.db import models

# Create your models here.

class URL(models.Model):
    full_url = models.TextField()
    hash = models.TextField(unique=True)

    class Meta:
        db_table = 'urlshorty'