from django.db import models


class History(models.Model):
    pub_date = models.DateTimeField('date published')
    rate = models.CharField(max_length=10)


class Currency(models.Model):
    name = models.CharField(max_length=3)
    history = models.ForeignKey(History, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
