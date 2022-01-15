from django.urls import path

from .views import ListPublicationsView, CreateFormsView, EditPublicationFormView, DeletePublicationView, ImportView, \
    ImportSingleBookView



urlpatterns = [
    path('', ListPublicationsView.as_view(), name="index"),
    path('add/', CreateFormsView.as_view(), name="add"),
    path('edit/<book_id>/', EditPublicationFormView.as_view(), name="edit"),
    path('delete/<book_id>/', DeletePublicationView.as_view(), name="delete"),
    path('import/', ImportView.as_view(), name="import"),
    path('import-book', ImportSingleBookView.as_view(), name='import_book')
]
