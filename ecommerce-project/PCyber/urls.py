from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:product_id>/<slug:product_slug>/', views.show_product, name='product_detail'),
    path('categories/', views.all_categories, name='all_categories'),
    path('products/category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('cart/', views.show_cart, name='show_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success_order, name='success_order'),
    path('sign-up/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
]