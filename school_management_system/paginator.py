from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
import abc


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_pages': self.page.paginator.num_pages,
            'total_items': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)), 
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'message':str(self.page.paginator.count) + ' ' + 'records found',
            'data': data

        })


