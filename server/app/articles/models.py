from django.db import models


class Article(models.Model):

    id = models.AutoField(primary_key=True)
    sid = models.CharField(max_length=25)
    sname = models.CharField(max_length=25)
    aid = models.CharField(max_length=20)
    headline = models.CharField(max_length=300)
    section = models.CharField(max_length=20)
    url = models.CharField(max_length=500)
    published_at = models.DateTimeField()

    class Meta:
        ordering = ['-published_at']
        unique_together = (('aid', 'sid'),)
