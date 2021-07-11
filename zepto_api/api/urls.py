from django.urls import path
# from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

library = views.LibraryCreateView.as_view({
    'get': 'list',
    'post': 'create'
})
library_pk = views.LibraryCreateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})
author = views.AuthorCreateView.as_view({
    'get': 'list',
    'post': 'create'
})
author_pk = views.AuthorCreateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})
book = views.BookCreateView.as_view({
    'get': 'list',
    'post': 'create'
})
book_pk = views.BookCreateView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})
urlpatterns = format_suffix_patterns([
    path("library/", library, name="library"),
    path("library/<int:pk>/", library_pk, name="library_pk"),
    path("library/list/", views.LibraryListUpdateView.as_view(), name="library_list"),

    path("author/", author, name="author"),
    path("author/<int:pk>/", author_pk, name="author_pk"),
    path("author/list/", views.AuthorListUpdateView.as_view(), name="author_list"),

    path("book/", book, name="book"),
    path("book/<int:pk>/", book_pk, name="book_pk"),
    path("book/list/", views.BookListUpdateView.as_view(), name="book_list"),
])

# router = DefaultRouter()
# router.register(r'v1/library', views.LibraryCreateView, basename='library')
# router.register(r'author', views.AuthorCreateView, basename='author')
# router.register(r'book', views.BookCreateView, basename='book')
# urlpatterns += router.urls