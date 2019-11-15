from django.db import models


class Article(models.Model):
    ORIGINS = [
        ('bbc', 'BBC'),
        ('nytimes', 'New York Times')
    ]

    title = models.CharField(max_length=200)
    insert_tsd = models.DateTimeField('Insert Timestamp')
    publish_tsd = models.DateTimeField('Published at')
    origin = models.CharField(max_length=50, choices=ORIGINS)
    original_url = models.URLField()
    bp1 = models.TextField()
    bp2 = models.TextField()
    bp3 = models.TextField()
    bp4 = models.TextField()
    bp5 = models.TextField()

    def __str__(self):
        return self.title
