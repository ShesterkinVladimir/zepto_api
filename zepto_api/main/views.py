# from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets

# from rest_framework.decorators import list_route
from .models import Library, Author, Book
from .serializers import LibraryListSerializer, AuthorListSerializer, BookListSerializer


# Library
# @list_route
class LibraryCreateView(viewsets.ModelViewSet):
    serializer_class = LibraryListSerializer
    queryset = Library.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



# class LibraryIdUpdateView(generics.RetrieveUpdateAPIView):
#
#     serializer_class = LibraryListSerializer
#     queryset = Library.objects.all()


class LibraryListUpdateView(APIView):  # можно ли уменьшить этот код?

    def get_object(self, pk):
        try:
            return Library.objects.get(pk=pk)
        except Library.DoesNotExist:
            raise Http404

    def put(self, request):
        for lib in request.data:
            library = self.get_object(pk=lib['id'])
            serializer = LibraryListSerializer(library, data=lib)
            if not serializer.is_valid():
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer.save()
            except AssertionError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        library = Library.objects.filter(id__in=[lib['id'] for lib in request.data])
        serializer = LibraryListSerializer(library, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        for lib in request.data:
            library = self.get_object(pk=lib['id'])
            serializer = LibraryListSerializer(library, data=lib, partial=True)
            if not serializer.is_valid():
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer.save()
            except AssertionError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        library = Library.objects.filter(id__in=[lib['id'] for lib in request.data])
        serializer = LibraryListSerializer(library, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Author
class AuthorCreateView(generics.ListCreateAPIView):

    serializer_class = AuthorListSerializer

    def get_queryset(self):
        queryset = Author.objects.all()
        lib = self.request.query_params.getlist('lib')
        if lib:
            queryset = queryset.filter(book__library__name__in=lib).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False

        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AuthorIdUpdateView(generics.RetrieveUpdateAPIView):

    serializer_class = AuthorListSerializer
    queryset = Author.objects.all()


class AuthorListUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def put(self, request):
        for aut in request.data:
            author = self.get_object(pk=aut['id'])
            serializer = AuthorListSerializer(author, data=aut)
            if not serializer.is_valid():
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer.save()
            except AssertionError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        author = Author.objects.filter(id__in=[aut['id'] for aut in request.data])
        serializer = AuthorListSerializer(author, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        for aut in request.data:
            author = self.get_object(pk=aut['id'])
            serializer = AuthorListSerializer(author, data=aut, partial=True)
            if not serializer.is_valid():
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer.save()
            except AssertionError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        author = Author.objects.filter(id__in=[aut['id'] for aut in request.data])
        serializer = AuthorListSerializer(author, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Book
class BookCreateView(generics.ListCreateAPIView):

    serializer_class = BookListSerializer
    queryset = Book.objects.all()

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False

        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookIdUpdateView(generics.RetrieveUpdateAPIView):

    serializer_class = BookListSerializer
    queryset = Book.objects.all()


class BookListUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def put(self, request):
        for bo in request.data:
            book = self.get_object(pk=bo['id'])
            serializer = BookListSerializer(book, data=bo)
            if not serializer.is_valid():
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer.save()
            except AssertionError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.filter(id__in=[bo['id'] for bo in request.data])
        serializer = BookListSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        for bo in request.data:
            book = self.get_object(pk=bo['id'])
            serializer = BookListSerializer(book, data=bo, partial=True)
            if not serializer.is_valid():
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer.save()
            except AssertionError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.filter(id__in=[bo['id'] for bo in request.data])
        serializer = BookListSerializer(book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





