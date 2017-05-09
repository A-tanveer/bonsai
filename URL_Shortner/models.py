from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShortenURL(models.Model):
    id = models.BigAutoField(primary_key=True)
    shortened_id = models.BigIntegerField(unique=True)
    short_url = models.CharField(unique=True, db_index=True)
    url = models.URLField()
    hits = models.ImageField(default=0)
    # created_by = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<Shortened URL (Hits %s): %s>"%(self.hits, self.url)


class URLVisits(models.Model):
    id = models.BigAutoField(primary_key=True)
    hits = models.ImageField(default=0)
    visit_date = models.DateTimeField(auto_now=True)
    from_country = models.CharField(max_length=45)
    referral = models.CharField(max_length=71)
    url_id_fk = models.ForeignKey(ShortenURL, on_delete=models.CASCADE)
