from django.contrib import admin
from .models import Balance, PersonalDetails, Transactions_history

# Register your models here.
admin.site.register(Balance)
admin.site.register(PersonalDetails)
admin.site.register(Transactions_history)