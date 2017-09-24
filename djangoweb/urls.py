"""djangoweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from webapp.views import Products, Home, search, ProductsCart, login, register, logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^products/$', Products.as_view(), name='productions'),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^addToCart/$', ProductsCart.as_view(), name='addToCart'),
    url(r'^search/$', search, name='search'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='tologin'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),
    url(r'^logout/$', logout, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
