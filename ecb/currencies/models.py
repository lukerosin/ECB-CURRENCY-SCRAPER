from django.db import models


class Currency(models.Model):
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Currencies'


class History(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    rate = models.CharField(max_length=10)
