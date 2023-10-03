from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20)
    publisher = models.CharField(max_length=100)
    page_count = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)  # Add this line for the price

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    outstanding_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return self.name

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Calculate the fee based on book price and quantity
        if not self.fee:
            self.fee = self.quantity * self.book.price
        super().save(*args, **kwargs)

    @property
    def calculate_outstanding_fees(self):
        # Calculate outstanding fees based on your logic
        # For example:
        return self.fee - self.member.outstanding_debt

    @property
    def returned_quantity(self):
        # Calculate the quantity of books that have already been returned
        # For example:
        return self.quantity - (self.quantity if self.return_date is None else 0)
