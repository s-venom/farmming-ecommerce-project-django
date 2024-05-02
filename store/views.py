from django.shortcuts import render
from .models import *

from django.http import JsonResponse #added3
import json

import datetime #for transId added 3

# added 4
from . utils import cookieCart, cartData, guestOrder

# Create your views here.

def home(request):
    # Add any data processing logic here
    return render(request, 'store/home.html')

#############################################

def store(request):
    data = cartData(request)  # Fetching cart data using the utility function

    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    # Reverse the order of products
    products = products[::-1]

    # Fetching the farmer/vendor for each product
    for product in products:
        product.farmer = product.farmer  # Fetching the related farmer/vendor instance

    cartItems = data['cartItems']

    context = {'products': products, 'cartItems': cartItems, 'categories': categories, 'shipping': False}
    return render(request, 'store/store.html', context)

##########################################

def profile(request):
    user = request.user
    user_profile = None
    farmer_products = None

    # Check if the user is a farmer
    if hasattr(user, 'farmer'):
        user_profile = user.farmer
        user_profile.is_customer = False
        farmer_products = Product.objects.filter(farmer=user.farmer)
    
    # Check if the user is a customer
    elif hasattr(user, 'customer'):
        user_profile = user.customer
        user_profile.is_customer = True
    
    context = {
        'user_profile': user_profile,
        'farmer_products': farmer_products
    }
    return render(request, 'store/profile.html', context)
######################################
from django.http import HttpResponseNotAllowed

def about_you(request):
    user = request.user
    user_profile = None

    # Check if the user is a farmer
    if hasattr(user, 'farmer'):
        user_profile = user.farmer
        user_profile.is_customer = False

    # Check if the user is a customer
    elif hasattr(user, 'customer'):
        user_profile = user.customer
        user_profile.is_customer = True


    if request.method == 'POST':
        if user_profile.is_customer:
            # CUST: Edit profile
            # Retrieve user data from form
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            phone = request.POST.get('phone')
            # Update user details
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user_profile.phone=phone
            user.save()
            user_profile.save()
            return redirect('/profile/about_you/')
        else:
            # FARMER: Edit profile
            # Retrieve user data from form
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            phone = request.POST.get('phone')
            shop_name = request.POST.get('shopName')
            address = request.POST.get('address')
            bank = request.POST.get('bank')
            image = request.FILES.get('image')
            # Update user details
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user_profile.phone=phone
            user_profile.shop_name=shop_name
            user_profile.address=address
            user_profile.bank=bank
            if 'image' in request.FILES:
                user_profile.image=image
            user.save()
            user_profile.save()
            return redirect('/profile/about_you/')
    
    # Render the 'about_you.html' template with the user profile data
    return render(request, 'store/about_you.html', {'user_profile': user_profile})
#####################
from django.shortcuts import get_object_or_404
from .forms import ProductForm

def my_products(request):
    categories = Category.get_all_categories()

    # Add Product
    if request.method == 'POST' and 'add_product_form' in request.POST:
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.farmer = request.user.farmer  # Assign the farmer instance here
            form.save()
            return redirect('/profile/my_products/')
    else:
        form = ProductForm()

    # Delete product
    if request.method == 'POST' and 'delete_product_id' in request.POST:
        product_id = request.POST.get('delete_product_id')
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return redirect('/profile/my_products/')
    
    # Handle product editing
    if request.method == 'POST' and 'edit_product_id' in request.POST:
        product_id = request.POST.get('edit_product_id')
        product = get_object_or_404(Product, id=product_id)
        
        # Update product details        
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.weight_quantity = request.POST.get('weight_quantity')
        product.digital = request.POST.get('digital') == 'on'
        product.stock = request.POST.get('stock')

        # Check if a new category is selected
        new_category_id = request.POST.get('categories')
        if new_category_id:
            product.categories = Category.objects.get(id=new_category_id)
        
        if 'image' in request.FILES:
            product.image = request.FILES.get('image')

        # Update more fields as needed
        product.save()
        return redirect('/profile/my_products/')
    
    farmer_products = Product.objects.filter(farmer=request.user.farmer).order_by('-id')
    return render(request, 'store/my_products.html', {'form': form, 'products': farmer_products, 'categories': categories})
#####################
def my_orders(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('-date_ordered')
    order_items = []
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        order_items.append((order, items))

    if request.method == 'POST':
        item_id = request.POST.get('delete_item_id')
        order_item = get_object_or_404(OrderItem, id=item_id)
        #if order.customer == request.user.customer:
        order_item.delete()
        return redirect('/profile/my_orders/')
    
    return render(request, 'store/my_orders.html', {'order_items': order_items})
#######################
def my_sales(request):
    order_items = OrderItem.objects.filter(product__farmer=request.user.farmer).order_by('-order__date_ordered')

    if request.method == 'POST' and 'order_item_id' in request.POST:
        # Handle order status update request
        item_id = request.POST.get('order_item_id')
        status = request.POST.get('status')
        order_item = get_object_or_404(OrderItem, id=item_id)
        order_item.status = status == 'completed'
        order_item.save()
        return redirect('/profile/my_sales/')

    if request.method == 'POST' and 'delete_item_id' in request.POST:
        # Handle delete order item request
        item_id = request.POST.get('delete_item_id')
        order_item = get_object_or_404(OrderItem, id=item_id)
        order_item.delete()
        return redirect('/profile/my_sales/')
    
    # Fetch shipping address for each order item
    for item in order_items:
        shipping_address = ShippingAddress.objects.filter(order=item.order).first()
        item.shipping_address = shipping_address
        print(shipping_address)

    return render(request, 'store/my_sales.html', {'order_items': order_items})
##########################################

def cart(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping':False}
    return render(request, 'store/cart.html', context)

##########################################

def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']    

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping':False}
    return render(request, 'store/checkout.html', context)

###########################################

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action =  data['action']

    print('Action ', action)
    print('ProductId ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

#######################################
#from django.views.decorators.csrf import csrf_exempt #added4
#@csrf_exempt

def processOrder(request):
    #print('Data:',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    #auth users only
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print('User is not logged in..')
        print('Cookies:', request.COOKIES)
        customer, order = guestOrder(request, data) # from utils.py
    
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    #shipping logic
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment Complete!', safe=False)



#####################################
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def loginPage(request):
    print('loginpage')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'store/login.html')

############################################
#from django.shortcuts import render, redirect
from django.contrib.auth.models import User
#from django.contrib.auth import authenticate, login
from django.contrib import messages

def signupPage(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Check if the email is already taken
        if User.objects.filter(username=email).exists():
            error = "Email is already taken"
            return render(request, 'store/signup.html', {'error': error})

        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)

        # Create the customer
        customer = Customer.objects.create(user=user, name=f"{first_name} {last_name}", email=email, phone=phone)

        messages.success(request, 'Your account has been created successfully. Please log in.')
        return redirect('/login/')  # Redirect to the login page after successful signup

    return render(request, 'store/signup.html')


#################################################
from django.contrib.auth import logout 

def logoutUser(request):
    logout(request)  
    return redirect('/home/')  

#################################################
from django.contrib.auth.decorators import login_required

#@login_required
def farmer_signup(request):
    if request.method == 'POST':
        # Extract data from the form
        shop_name = request.POST.get('shop_name')
        bank = request.POST.get('bank')
        address = request.POST.get('address')
        image = request.FILES.get('image')

        # Create a new farmer object
        user = request.user  # Get the logged-in user
        farmer = Farmer.objects.create(user=user, image=image, shop_name=shop_name, bank=bank, address=address)

        # Redirect to some success page or message
        return redirect('/')  # Redirect to farmer's dashboard or any other page
        
    else:
        if request.user.is_authenticated:
            # User is already logged in as a customer
            return render(request, 'store/farmer_signup.html', {'message': 'Hi, thank you for your interest in becoming a farmer! Please provide the necessary details below.'})
        else:
            # User is not logged in, redirect to customer signup page
            return render(request, 'store/signup.html', {'message': 'Please sign in as a customer first.'})  # Assuming '/signup/' is the URL for customer signup page

