from django.conf.urls import url

from ..articles import views


urlpatterns = [
    url(r'^v1/articles/', views.articles, name='articles'),
    url(r'^v1/sources/', views.sources, name='articles-sources'),
]
