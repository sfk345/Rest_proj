from django.urls import path
from .views import *


urlpatterns = [
    path('', Home, name='home'),
    path('books/', AllBooks.as_view(), name='all_books'),
    path('book/<pk>', DitailBooks.as_view(), name='detail_book'),
    path('book/field/<pk>', BookSearch.as_view(), name='book_search'),
    path('authors/', AllAuthors.as_view(), name='all_authors'),
    path('author/<pk>', DitailAuthors.as_view(), name='detail_author')

]

# {"get": "list"}

