from django.contrib import admin

# Register your models here.
from .models import Author, Publication


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'author')


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'isbn', 'publication_date', 'publication_date_type',
                    'book_cover', 'language', 'page_count')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Publication, PublicationAdmin)
