from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShortenURL(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.URLField()
    shortened_id = models.BigIntegerField(default=0)
    short_url = models.CharField(default='', max_length=10)
    hits = models.IntegerField(default=0)
    # created_by = models.ForeignKey(User, related_name='created by')
    date_created = models.DateTimeField(auto_now=True, editable=False)

    def __repr__(self):
        return "<Shortened URL (Hits %s): %s>"%(self.hits, self.url)


class HitsDatePoint(models.Model):
    day = models.DateField(auto_now=True, db_index=True)
    hits = models.IntegerField(default=0)
    link = models.ForeignKey(ShortenURL)

    class Meta:
        unique_together = (("day", "link"),)


class URLVisits(models.Model):
    id = models.BigAutoField(primary_key=True)
    visit_date = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField()
    # from_country = models.CharField(max_length=45)
    # referral = models.CharField(max_length=71)  # will do it later
    url_id_fk = models.ForeignKey(ShortenURL, on_delete=models.CASCADE)
