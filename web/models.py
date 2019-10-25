from django.db import models


class Article(models.Model):
    ORIGINS = [
        ('bbc', 'BBC'),
    ]

    title = models.CharField(max_length=200)
    insert_tsd = models.DateTimeField('Insert Timestamp')
    origin = models.CharField(max_length=50, choices=ORIGINS)
    bp1 = models.TextField()
    bp2 = models.TextField()
    bp3 = models.TextField()
    bp4 = models.TextField()
    bp5 = models.TextField()

    def __str__(self):
        return self.title
