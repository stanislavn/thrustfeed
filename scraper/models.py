from django.db import models


class Product(models.Model):
    availability    = models.CharField(max_length=200, blank = True, null=True)
    itemCondition   = models.CharField(max_length=200, blank = True, null=True)
    price           = models.FloatField(max_length=200, blank = True, null=True)
    priceCurrency   = models.CharField(max_length=200, blank = True, null=True)
    url             = models.URLField(max_length=2200, unique=True)
    brand           = models.CharField(max_length=200, blank = True, null=True)
    color           = models.CharField(max_length=900, blank = True, null=True)
    depth           = models.CharField(max_length=400, blank = True, null=True)
    gtin12          = models.CharField(max_length=200, blank = True, null=True)
    logo            = models.URLField(max_length=2200, blank = True, null=True)
    manufacturer    = models.CharField(max_length=900, blank = True, null=True)
    mpn             = models.CharField(max_length=900, blank = True, null=True)
    sku             = models.CharField(max_length=900, blank = True, null=True)
    alternateName   = models.CharField(max_length=900, blank = True, null=True)
    description     = models.CharField(max_length=2200, blank = True, null=True)
    image           = models.URLField(max_length=2200, blank = True, null=True)
    name            = models.CharField(max_length=900, blank = True, null=True)
    compatible      = models.CharField(max_length=2200, blank = True, null=True)

    def __str__(self):
        return self.name