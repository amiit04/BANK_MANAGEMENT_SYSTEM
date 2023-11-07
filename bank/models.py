from django.db import models

# Create your models here.
class Balance(models.Model):
    account_number = models.CharField(max_length=10, unique=True, primary_key=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return self.account_number


class PersonalDetails(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=7, unique=True)
    account_number = models.CharField(max_length=10, primary_key=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.TextField()
    mobile_number = models.CharField(max_length=10)
    pin_code = models.CharField(max_length=6)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Transactions_history(models.Model):
    to_account_number = models.CharField(max_length=10)
    from_account_number = models.CharField(max_length=10)
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    typee = models.CharField(max_length=6)

    def __str__(self):
        return self.to_account_number + ' ' + str(self.amount)
