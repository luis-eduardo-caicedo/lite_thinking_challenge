from django.db import models
from apps.companies.models import Company
from djmoney.models.fields import MoneyField


class Product(models.Model):
    code       = models.CharField(max_length=20)
    name       = models.CharField(max_length=100)
    features   = models.TextField()
    price      = MoneyField(max_digits=14,
                            decimal_places=2,
                            default_currency='USD')
    company    = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} – {self.code}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
