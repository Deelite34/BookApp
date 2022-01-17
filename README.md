![image](https://user-images.githubusercontent.com/35972878/149679485-5f206652-a977-4700-ae36-5a87c2c0e48f.png)

## BookApp
Django project, allowing user to list, create, edit, delete, search and import books from google book api.
Uses bootstrap for frontend, and also offers rest api.  
Interface text uses Polish language.

# Features
- Uses Django, DRF, and bootstrap
- All books are displayed in a table, with edit and delete buttons for each book.
- You can filter books using a form on the main page
- Books can be either added using a form in designated subpage, or imported from <a href="https://www.googleapis.com/books/v1/volumes">google book api</a>, also with form.
- Rest API other than standard crud operations, allows user to search or filter books with use of query strings. Search endpoint accepts single 'search' keyword used to search all fields of author or book, while filter endpoint allows you to filter each field with addition of filtering publication_before and publication_after.
- Tests with django unittest

# Live preview
Todo

# Installation
create virtual environment `python -m venv venv_bookapp`  
launch virtual environment `.\venv_bookapp\scripts\activate`  
Install required modules `pip install -r requirements.txt`  
Apply migrations `python manage.py migrate`  
Run app `python manage.py runserver`  

## Tests
Tests using django unittest module can be ran with `python manage.py test`

## Endpoint documentation

- Download schema.yml and go to https://editor.swagger.io/  
- Import schema.yml file with file->import file  

Alternatively  
- Copy content of schema.yml file and go to https://editor.swagger.io/  
- Paste it in the editor on the left side   
