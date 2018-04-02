"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from authen import views as index_views

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page

from authen.models import UserProfile

sitemaps = {
    'bbs': GenericSitemap({'queryset': UserProfile.objects.all()}, priority=0.6),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authen.urls')),
    path('', index_views.IndexView.as_view(), name='index'),
    path('oauth/', include('oauth.urls')),
    # path('sitemaps\.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
    path('sitemaps.xml', cache_page(86400)(sitemaps_views.index), {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    path('sitemaps-<str: section>.xml', cache_page(86400)(sitemaps_views.sitemap), {'sitemaps': sitemaps}, name='sitemaps'),

]
