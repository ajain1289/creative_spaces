"""creative_spaces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from backend_app import views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend_app.urls', namespace='backend')),
    path('professional/', include('professionals.urls', namespace='professionals')),
    path('user/', include('users.urls', namespace='users')),
    path('verify/', views.user_verification, name='verify'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('forgot_password_verify/', views.forgot_password_verification, name='forgot_password_verification'),
    path('logout/', views.my_logout, name="logout"),
    path('payment_processing/', views.payment_processing, name='payment_processing'),
    path('payment_successful/', views.payment_successful, name='payment_successful'),
    path('payment_failed/', TemplateView.as_view(template_name='payment_failed'), name='payment_failed'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
