from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from .models import Book
from .serializers import BooksSerializers, AuthorsSerializers


def Home(request):
    return render(request, 'home_page.html')


class AllBooks(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BooksSerializers

    def post(self, request):
        serializer = BooksSerializers

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            if (AllBooks.objects.get(title=request.data['title']).publisher != request.data['publisher'] and request.data[
                'genre'] == 'художественное произведение переведенное с другого языка'): serializer.is_valid()
            if (AllBooks.objects.get(title=request.data['title']).yearOfRel != request.data['yearOfRel'] and request.data[
                'genre'] == 'учебник'):
                serializer.is_valid()
            else:
                raise Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DitailBooks(APIView):
    def get(self, request, pk):
        books = AllBooks.objects.get(pk=pk)
        serializer = BooksSerializers(books)
        return Response(serializer.data)


class BookSearch(APIView):
    def get(self, request, field, property):
        try:
            if field == 'title':
                book = AllBooks.objects.filter(title=property)
            elif field == 'genre':
                book = AllBooks.objects.filter(genre=property)
            elif field == 'author':
                book = AllBooks.objects.filter(author=property)
        except AllBooks.DoesNotExist:
            return HttpResponse(status=404)


class AllAuthors(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        author = AllAuthors.objects.all()
        serializer = AuthorsSerializers(author, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorsSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class DitailAuthors(APIView):
    def get(self, request, pk):
        author = AllAuthors.objects.get(pk=pk)
        serializer = AuthorsSerializers(author)
        return Response(serializer.data)
