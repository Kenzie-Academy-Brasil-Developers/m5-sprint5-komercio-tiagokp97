from django.db import models
from django.core.validators import MinValueValidator

MIN = 1
class Product(models.Model):
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(MIN)])
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey("accounts.Account", on_delete=models.CASCADE, related_name='products')
