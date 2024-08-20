from collections import defaultdict

from rest_framework.filters import OrderingFilter as DRFOrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class OrderingFilter(DRFOrderingFilter):

    def get_params(self, request, view):
        """
        get param from order field mapping.
        This function is used for find the ordering field in case of normal model or in case of relational model
        """
        params = request.query_params.get(self.ordering_param)
        ordering_fields_mapping = getattr(view, 'ordering_fields_mapping', None)

        if not params:
            return

        if ordering_fields_mapping:

            ordering_fields = getattr(view, 'ordering_fields', [])
            if isinstance(ordering_fields, str):
                ordering_fields = [ordering_fields]

            view.ordering_fields = ordering_fields + type(ordering_fields)(ordering_fields_mapping.values())

            return [
                '-' + ordering_fields_mapping[params[1:]] if param[0] == '-' else ordering_fields_mapping[params]
                for param in params.split(',')
            ]

        return params.split(',')

    def get_ordering(self, request, queryset, view):
        params = self.get_params(request, view)
        if params:
            fields = [param.strip() for param in params]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering

        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view)


class FilterBackend(DjangoFilterBackend):

    def get_filterset(self, request, queryset, view):

        _filterset_fields = defaultdict(set)
        query_params = request.query_params.copy()
        filterset_fields = getattr(view, 'filterset_fields', None)
        filterset_fields_mappings = getattr(view, 'filterset_fields_mappings', None)

        if filterset_fields_mappings:
            for _name, _filter in filterset_fields_mappings.items():
                field_name, lookup_expr = _filter, ''

                if type(_filter) in (tuple, list):
                    field_name, lookup_expr = _filter
                _filterset_fields[field_name].add(lookup_expr or 'exact')

                if _name in query_params and field_name != _name:
                    _value = query_params[_name]
                    query_params.pop(_name)
                    if not lookup_expr:
                        query_params[field_name] = _value
                    else:
                        query_params[field_name+"__"+lookup_expr] = _value

        if filterset_fields and type(filterset_fields) in (tuple, list):
            _filterset_fields.update({
                f: set(_filterset_fields[f]) | {'exact'} for f in filterset_fields
            })

        if _filterset_fields:
            view.filterset_fields = _filterset_fields
            # view.filterset_fields = {f:list(v) for f,v in _filterset_fields}

        filterset_class = self.get_filterset_class(view, queryset)

        if filterset_class is None:
            return None

        # kwargs = self.get_filterset_kwargs(request, queryset, view)
        kwargs = {
            'data': query_params,
            'queryset': queryset,
            'request': request,
        }
        return filterset_class(**kwargs)
