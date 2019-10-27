"""geekHouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from werobot.contrib.django import make_view
from apps.wxRobot import robot_instance
from django.contrib.staticfiles.views import serve
from django.contrib.sitemaps.views import sitemap
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from sitemap import BookDetailSiteMap
from apps.eBook.urls import html_urlpatterns
from django.views.decorators.cache import cache_page

sitemaps = {
    'book': BookDetailSiteMap,
}

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^favicon.ico$', favicon_view),
    url(r'^robots\.txt', TemplateView.as_view(template_name="html/roboots.html"), name="robots"),
    url(r'^sitemap.xml$', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^api/admin/', admin.site.urls),

    url(r'^api/', include('eBook.urls', 'eBook')),
    url(r'^api/', include('movie.urls', 'movie')),
    url(r'^api/', include('school.urls', 'school')),
    url(r'^api/', include('society.urls', 'society')),
    url(r'^wx/', make_view(robot_instance)),
    url(r'', include(html_urlpatterns)),
    url(r'(?!api)', TemplateView.as_view(template_name="index.html"), name="web"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
