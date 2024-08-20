from collections import OrderedDict
import inspect

from django.core.paginator import InvalidPage
from django.utils.inspect import method_has_no_args
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param

class BasePagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = '_page_size'
    page_query_param = '_page'
    #max_page_size = 10000

    def _get_count(self, object_list):
        """Return the total number of objects, acrospaginate_querysets all pages."""
        c = getattr(object_list, 'count', None)
        if callable(c) and not inspect.isbuiltin(c) and method_has_no_args(c):
            return c()
        return len(object_list)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        # edited
        # added to get count of queryset
        self._count = self._get_count(queryset)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            # edited
            # commented to avoid error

            # msg = self.invalid_page_message.format(
            #     page_number=page_number, message=six.text_type(exc)
            # )
            # raise NotFound(msg)
            return list()

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_next_link(self):
        # edited
        # added to avoid no attr page
        if not hasattr(self, 'page'):
            return None
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_previous_link(self):
        # edited
        # added to avoid no attr page
        if not hasattr(self, 'page'):
            return None
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.page.previous_page_number()
        if page_number == 1:
            return remove_query_param(url, self.page_query_param)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self._count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))