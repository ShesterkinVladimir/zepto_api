from django.db import models


class Library(models.Model):
    address = models.CharField(max_length=256)
    book_capacity = models.PositiveIntegerField()
    name = models.CharField(max_length=128)


class Author(models.Model):
    name = models.CharField(max_length=128)
    birth_date = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    name = models.CharField(max_length=128)
    year = models.SmallIntegerField(null=True)
    authors = models.ManyToManyField(Author)
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="library_book")



