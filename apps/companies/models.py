from django.db import models


class Company(models.Model):
    nit       = models.CharField(max_length=20, primary_key=True)
    name      = models.CharField(max_length=100)
    address   = models.CharField(max_length=200)
    phone     = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Company" 
        verbose_name_plural = "Companies" 