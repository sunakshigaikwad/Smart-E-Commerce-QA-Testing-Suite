from django.db import models

# models.py
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    reviews = models.IntegerField()
    delivery = models.CharField(max_length=100, default='Standard Delivery')

    # ✅ Add this line
    category = models.CharField(max_length=100, default='General')

class Transaction(models.Model):
    user = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)  # "Success" / "Failed"
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.status} - ₹{self.amount}"
    
