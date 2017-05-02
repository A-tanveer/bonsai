from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShortenURL(models.Model):
    id = models.BigAutoField(primary_key=True)
    shortened_id = models.BigIntegerField(unique=True)
    url = models.CharField(max_length=2083) # this should be url field
    created_by = models.ForeignKey(User)
    date_created = models.DateTimeField('date when URL was shortened')


class URLVisits(models.Model):
    id = models.BigAutoField(primary_key=True)
    visit_date = models.DateTimeField('date visited')
    from_country = models.CharField(max_length=45)
    referral = models.CharField(max_length=71)
    url_id_fk = models.ForeignKey(ShortenURL, on_delete=models.CASCADE)
