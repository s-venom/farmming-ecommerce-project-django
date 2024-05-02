from django.urls import path

from . import views


urlpatterns = [
    #Leave as empty string for base url
	path('', views.store, name="store"),
    path('home/', views.home, name="home"),
    #path('', views.home, name="home"),
    
	path('login/', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('farmer_signup/', views.farmer_signup, name='farmer_signup'),
    
	#path('store/', views.store, name="store"),
	path('profile/', views.profile, name="profile"),
    path('profile/about_you/', views.about_you, name='about_you'),
    path('profile/my_products/', views.my_products, name='my_products'),
    path('profile/my_orders/', views.my_orders, name='my_orders'),
    path('profile/my_sales/', views.my_sales, name='my_sales'),


	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    
	path('update_item/', views.updateItem, name="update_item"), #added3
	path('process_order/', views.processOrder, name="process_order"),
]