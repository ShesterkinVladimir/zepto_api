from django.urls import path

from . import views

urlpatterns = [
    path("library/", views.LibraryCreateView.as_view(), name="library"),
    path("library/<int:pk>/", views.LibraryIdUpdateView.as_view(), name="library_pk"),
    path("library/list/", views.LibraryListUpdateView.as_view(), name="library_list"),

    path("author/", views.AuthorCreateView.as_view(), name="author"),
    path("author/<int:pk>/", views.AuthorIdUpdateView.as_view(), name="author_pk"),
    path("author/list/", views.AuthorListUpdateView.as_view(), name="author_list"),

    path("book/", views.BookCreateView.as_view(), name="book"),
    path("book/<int:pk>/", views.BookIdUpdateView.as_view(), name="book_pk"),
    path("book/list/", views.BookListUpdateView.as_view(), name="book_list"),
]
