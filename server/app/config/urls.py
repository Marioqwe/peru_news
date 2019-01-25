from django.contrib import admin
from django.conf.urls import url

from ..articles import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/articles/', views.articles, name='articles'),
    url(r'^api/v1/sources/', views.sources, name='articles-sources'),
]
