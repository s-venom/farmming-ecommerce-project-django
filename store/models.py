from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)
	phone = models.CharField(max_length=15, null=True, blank=True)

	def __str__(self):
		return self.name
	
	@staticmethod
	def get_customer_by_email(email):
		try:
			return Customer.objects.get(email=email)
		except Customer.DoesNotExist:
			return None
		
	def isExists(self):
		return Customer.objects.filter(email=self.email).exists()	

class Farmer(models.Model): 
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	image = models.ImageField(null=True, blank=True)
	shop_name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=15, null=True, blank=True)
	bank = models.PositiveIntegerField()
	address = models.CharField(max_length=200, null=True, blank=True)
	
	def __str__(self):
		return self.shop_name
	
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url	

class Category(models.Model):
	#Model for product categories.
	name = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.name

	@staticmethod
	def get_all_categories():
		return Category.objects.all()

class Product(models.Model):
	#Model for individual farming products.
	farmer = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True)  # Link product to a Farmer
	categories = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	price = models.FloatField()
	weight_quantity = models.CharField(max_length=50, blank=True)  # Can be weight, unit count, etc.
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True, upload_to='store/product/')
	stock = models.PositiveIntegerField(null=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url	
	
	@staticmethod
	def get_products_by_id(ids):
		return Product.objects.filter (id__in=ids)
	
	@staticmethod
	def get_all_products():
		return Product.objects.all()
	
	@staticmethod
	def get_all_products_by_categoryid(category_id):
		#if category_id:
		#	return Product.objects.filter (category=category_id)
		#else:
		#	return Product.get_all_products();
		if category_id:
			return Product.objects.filter(categories=category_id)
		else:
			return Product.get_all_products()

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

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
	status = models.BooleanField(default=False)

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
