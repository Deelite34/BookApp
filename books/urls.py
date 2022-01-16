from django.urls import path, include

from .views import ListPublicationsView, CreateFormsView, \
    EditPublicationFormView, DeletePublicationView, ImportView, \
    ImportSingleBookView

urlpatterns = [
    path('', ListPublicationsView.as_view(), name="index"),
    path('add-book', CreateFormsView.as_view(), name="add"),
    path('edit-book/<book_id>', EditPublicationFormView.as_view(),
         name="edit"),
    path('delete-book/<book_id>', DeletePublicationView.as_view(),
         name="delete"),
    path('import', ImportView.as_view(), name="import"),
    path('import-book', ImportSingleBookView.as_view(), name='import_book'),
    path('api', include('api.urls'), name='publication_viewset')
]
