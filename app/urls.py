from django.urls import path,include
from .import views
urlpatterns = [

    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    path('register', views.register, name='create_user'),
    path('success/', views.success, name='success'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('product/', views.product_list, name='product_list'),
    path('users/', views.user_list, name='user_list'),
    path('addproduct/', views.add_product, name='add_product'),
    path('login/', views.login_view, name='login'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),        
    path('products/', views.user_product_list, name='user_product_list'),
    path('add_cart/<int:pid>/',views.add_cart,name='add_cart'),
    path('cart_list/',views.cart_list,name='cart_list'),
    path('delete_cartlist/<int:id>/', views.delete_cart_item, name='delete_cart_item'),
path('wishlist_toggle/<int:pid>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('product_details/<int:pid>/', views.product_detail, name='product_details'),
    path("add_review/<int:pid>/", views.add_review, name="add_review"),
     path('initiate-payment/<cid>/', views.initiate_payment, name='initiate-payment'),
    path('confirm-payment/<order_id>/<payment_id>/<crti_id>/', views.confirm_payment, name='confirm-payment'),
    path("delete_cartlist/<int:item_id>/", views.delete_cartlist, name="delete_cartlist"),
    path("search/", views.search_products, name="search"),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
     path("wishlist/", views.wishlist_page, name="wishlist_page"),
    path('logout/', views.logout_view, name='logout'),

    



    ]