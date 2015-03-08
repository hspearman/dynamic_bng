"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url, include
from rest_framework import routers
from app import apis
from app import views

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin', include(router.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^bands/random$', apis.bands_random),
    url(r'^spotify/authorize$', apis.spotify_authorize),
    url(r'^spotify/authorize/status$', apis.spotify_is_authorized)
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
