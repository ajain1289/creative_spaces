from django.urls import path
from backend_app import views
from backend_app.apps import BackendAppConfig

app_name = BackendAppConfig.name

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('products/', views.products, name='products'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('update_password/', views.UpdatePassword.as_view(), name='update_password'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('update_my_profile/', views.update_my_profile, name='update_my_profile'),
    path('add_product/', views.AddProduct.as_view(), name='add_product'),
    path('login/', views.MyLogin.as_view(), name='login'),
    path('register/', views.AdminRegistration.as_view(), name='admin_registration'),
    path('admin_index/', views.admin_index, name='admin_index'),
    path('view_products/', views.view_products, name='view_products'),
    path('add_category/', views.add_category, name='add_category'),
    path('view_categories/', views.view_categories, name='view_categories'),
    path('update_category/<int:pk>/', views.update_category, name='update_category'),
    path('qty_increase_decrease/', views.qty_increase_decrease, name='qty_increase_decrease'),
    path('checkout_page/', views.checkout_page, name='checkout_page'),
    path('delete_cart_item/<int:pk>/', views.delete_cart_item, name='delete_cart_item'),
    path('delete_category/<int:pk>/', views.delete_category, name='delete_category'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
]