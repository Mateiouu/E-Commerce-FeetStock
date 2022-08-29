from django.db import models
from django.db.models import Q

# Create your models here.

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

# class Customer(models.Model):
# 	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
# 	name = models.CharField(max_length=200, null=True, blank=True)
# 	email = models.CharField(max_length=200, null=True, blank=True)
# 	device = models.CharField(max_length=200, null=True, blank=True)

# 	def __str__(self):
# 		if self.name:
# 			name = self.name
# 		else:
# 			name = self.device
# 		return str(name)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200, blank= True, null = True)
    profilepic = models.ImageField(blank= True, null = True)
    description = models.CharField(max_length=200, blank= True, null = True)
    device = models.CharField(max_length=200, blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add= True, null = True)

@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_customer(sender, instance, **kwargs):
    instance.customer.save()


class Product(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	sex = models.CharField(max_length=20,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)


	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	
	class Meta:
		constraints = [
            models.UniqueConstraint(
                fields=('customer',),
                condition=Q(complete=False),
                name='incomplete_order_per_customer',
            )
        ]
		

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

	

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address