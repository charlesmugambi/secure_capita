from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone

class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = (
        ('Individual', 'Individual'),
        ('Institution', 'Institution'),
    )
    
    CUSTOMER_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='Individual')
    status = models.CharField(max_length=20, choices=CUSTOMER_STATUS_CHOICES, default='Active')

    def __str__(self):
        return self.name



class Invoice(models.Model):
    INVOICE_STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled')
    )
    invoice_number = models.CharField(max_length=8, unique=True, editable=False)
    invoice_date = models.DateField()
    due_date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invoices',null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS_CHOICES, default='Draft')
    
    @property
    def subtotal(self):
        return sum(item.total_price() for item in self.items.all())
    @property
    def discount_amount(self):
        if self.discount is not None and self.discount > 0:
            return self.subtotal * (self.discount / 100)
        return 0
    
    @property
    def total_before_discount(self):
        return self.subtotal
    
    @property
    def total_after_discount(self):
        total = self.subtotal - self.discount_amount
        return round(total, 2)
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        if not self.invoice_date:
            self.invoice_date = timezone.now().date()
        super().save(*args, **kwargs)
    
    def generate_invoice_number(self):
        prefix = 'INV'
        characters = string.digits
        random_part = ''.join(random.choices(characters, k=5))  # Generate 17 random digits
        return prefix + random_part  # Generate a 10-character random string
        
    def __str__(self):
        return self.invoice_number

class InvoiceItem(models.Model):
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=100, decimal_places=2)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', null=False, blank=True)

    def total_price(self):
        return self.quantity * self.unit_price







