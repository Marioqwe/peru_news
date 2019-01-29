from django.contrib import admin
from django.conf.urls import url

from ..articles import views


urlpatterns = [
    # REST API
    url(r'^v1/articles/', views.articles, name='articles'),
    url(r'^v1/sections/', views.sections, name='articles-sections'),
    url(r'^v1/sources/', views.sources, name='articles-sources'),

    # Django Admin
    url(r'^admin/', admin.site.urls),
]
