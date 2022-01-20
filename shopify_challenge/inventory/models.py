from django.db import models

class Product(models.Model):
    product_name = models.TextField(max_length=50, default="")
    product_description = models.TextField(max_length=200, default="")
    product_msrp = models.DecimalField(max_digits=6,decimal_places=2)
    product_code = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product_name

class City(models.Model):
    city_name = models.TextField(max_length=20, default="")
    state = models.TextField(max_length=2, default="")
    zipcode = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.city_name


class Warehouse(models.Model):
    warehouse_name = models.TextField(max_length=50, default="")
    address = models.TextField(max_length=50, default="")
    city_id = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return self.warehouse_name

class Stock(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    warehouse_id = models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

