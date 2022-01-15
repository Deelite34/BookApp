from django.db import router
from django.urls import path, include
from rest_framework import routers

from .views import PublicationFilterViewSet, AuthorFilterViewSet, PublicationSearchViewSet, AuthorSearchViewSet, \
    PublicationViewSet, AuthorViewSet

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'publications', PublicationViewSet)

filter_router = routers.DefaultRouter()
filter_router.register(r'authors', AuthorFilterViewSet)
filter_router.register(r'publications', PublicationFilterViewSet)

search_router = routers.DefaultRouter()
search_router.register(r'authors', AuthorSearchViewSet)
search_router.register(r'publications', PublicationSearchViewSet)


urlpatterns = [
    path('/', include(router.urls)),
    path('/filter/', include(filter_router.urls)),
    path('/search/', include(search_router.urls)),

]