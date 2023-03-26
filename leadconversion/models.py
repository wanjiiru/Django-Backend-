from django.contrib.auth.models import User
from django.db import models


class UserRole(User):
    role_options = (
        ('lead-creator', 'Lead Creator'),
        ('customer-creator', 'Customer Creator'),
    )
    role = models.CharField(max_length=255, choices=role_options)

    @classmethod
    def get_all(cls):
        return UserRole.objects.all()

    def __str__(self) -> str:
        return self.username


class Lead(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    gender = models.CharField(max_length=1)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='leads')

    def __str__(self) -> str:
        return f"{self.first_name}, {self.last_name}"

    @classmethod
    def get_all(cls):
        return Lead.objects.all()

    @classmethod
    def get_name(cls, first_name):
        return Lead.objects.get(first_name)

    @classmethod
    def get_id(cls, id):
        return Lead.objects.get(id=id)


class Product(models.Model):
    name = models.CharField(max_length=255,unique=True)

    @classmethod
    def get_id(cls, id):
        return Product.objects.get(id=id)

    @classmethod
    def get_all(cls):
        return Product.objects.all()

    @classmethod
    def get_by_name(cls, name):
        return Product.objects.get(name=name)


class Customer(models.Model):
    created_by = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='customers')
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='customer_photos/', blank=True)
    annual_earning = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    products_of_interest = models.ManyToManyField(Product)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.lead.first_name}, {self.lead.last_name}"

    @classmethod
    def get_all(cls):
        return Customer.objects.all()

    @classmethod
    def get_id(cls, id):
        return Customer.objects.get(id = id)
