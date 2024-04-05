from django.db import models


class Song(models.Model):
    tags = models.CharField(max_length=256, blank=True, null=True)
    theme = models.CharField(max_length=256, blank=True, null=True)
    genretype = models.CharField(max_length=256, blank=True, null=True)
    genre = models.CharField(max_length=256, blank=True, null=True)
    author = models.CharField(max_length=256, blank=True, null=True)
    creationyear = models.CharField(max_length=256, blank=True, null=True)
    composer = models.CharField(max_length=256, blank=True, null=True)
    fullname = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return f"{self.author} - {self.fullname}"
