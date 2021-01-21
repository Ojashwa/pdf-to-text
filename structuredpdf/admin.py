from django.contrib import admin
from .models import Userpdfdata,Userregistration

# Register your models here.
@admin.register(Userregistration)
class UserRegistration(admin.ModelAdmin):
    fields =('name','email','password')
@admin.register(Userpdfdata)
class UserpdfData(admin.ModelAdmin):
    fields=('seller','buyer','invoice_number','invoice_date','items','digitalized')