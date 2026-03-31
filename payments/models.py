from django.db import models

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    )

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    reference = models.CharField(max_length=100, unique=True, help_text="Gateway-agnostic transaction reference")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.reference} for Order {self.order.id}"
