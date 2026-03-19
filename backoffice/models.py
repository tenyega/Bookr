from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField()
    
    def __unicode__(self):
        return f"{self.name} [{self.code}]"

class ProductItem(models.Model):
    color   = models.CharField(max_length=100)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    code    = models.IntegerField()
    
    def __unicode__(self):
        return f"{self.product.name} {{self.color}} [{self.code}]"