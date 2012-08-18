from django.db import models


class Test(models.Model):
    title = models.CharField('Title', max_length=255)
