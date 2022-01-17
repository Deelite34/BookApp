from django.urls import path, include
from rest_framework import routers

from .views import PublicationFilterViewSet, AuthorFilterViewSet, \
    PublicationSearchViewSet, AuthorSearchViewSet, \
    PublicationViewSet, AuthorViewSet

# All CRUD operations
router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'publications', PublicationViewSet)

# Read only operations + filtering
filter_router = routers.DefaultRouter()
filter_router.register(r'authors', AuthorFilterViewSet,
                       basename='filter-authors')
filter_router.register(r'publications', PublicationFilterViewSet,
                       basename='filter-publications')
# Read only operations + searching
search_router = routers.DefaultRouter()
search_router.register(r'authors', AuthorSearchViewSet,
                       basename='search-authors')
search_router.register(r'publications', PublicationSearchViewSet,
                       basename='search-publications')

urlpatterns = [
    path('/', include(router.urls)),
    path('/filter/', include(filter_router.urls)),
    path('/search/', include(search_router.urls)),
]
