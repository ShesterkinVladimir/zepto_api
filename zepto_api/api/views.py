from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets, permissions
from django_filters import BaseInFilter, CharFilter, FilterSet


from .models import Library, Author, Book
from .serializers import LibraryListSerializer, AuthorListSerializer, BookListSerializer


# filter for authors by libraries
class CharInFilter(BaseInFilter, CharFilter):
    pass


class DataFilter(FilterSet):
    library = CharInFilter(field_name='book__library__name', lookup_expr='in', label='library')

    class Meta:
        model = Author
        fields = []


# Library

class BulkCommonView(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.request.method in ['DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(BulkCommonView, self).get_serializer(*args, **kwargs)


class UpdateList(APIView):

    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        serializer_class = kwargs.pop('serializer_class')
        model = kwargs.pop('model')
        for data in request.data:
            obj = get_object_or_404(model, pk=data.get('id'))
            serializer = serializer_class(obj, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        obj = model.objects.filter(id__in=[lib.get('id') for lib in request.data])
        serializer = serializer_class(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)


class LibraryCreateView(BulkCommonView):
    serializer_class = LibraryListSerializer
    queryset = Library.objects.all()


class LibraryListUpdateView(UpdateList):

    def put(self, request, *args, **kwargs):
        kwargs['serializer_class'] = LibraryListSerializer
        kwargs['model'] = Library
        return super(LibraryListUpdateView, self).put(request, *args, **kwargs)

    def patch(self, request,  *args, **kwargs):
        kwargs['serializer_class'] = LibraryListSerializer
        kwargs['model'] = Library
        return super(LibraryListUpdateView, self).patch(request,  *args, **kwargs)


# Author
class AuthorCreateView(BulkCommonView):

    serializer_class = AuthorListSerializer
    queryset = Author.objects.all()
    filterset_class = DataFilter


class AuthorListUpdateView(UpdateList):

    def put(self, request, *args, **kwargs):
        kwargs['serializer_class'] = AuthorListSerializer
        kwargs['model'] = Author
        return super(AuthorListUpdateView, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['serializer_class'] = AuthorListSerializer
        kwargs['model'] = Author
        return super(AuthorListUpdateView, self).patch(request, *args, **kwargs)


# Book
class BookCreateView(BulkCommonView):

    serializer_class = BookListSerializer
    queryset = Book.objects.all()


class BookListUpdateView(UpdateList):

    def put(self, request, *args, **kwargs):
        kwargs['serializer_class'] = BookListSerializer
        kwargs['model'] = Book
        return super(BookListUpdateView, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs['serializer_class'] = BookListSerializer
        kwargs['model'] = Book
        return super(BookListUpdateView, self).patch(request, *args, **kwargs)





