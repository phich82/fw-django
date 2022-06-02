from django.utils import timezone

class BaseService:

    def resolve_id_and_params(self, id, params):
        pk = None
        if len(id) > 0:
            pk = id[0]
            if 'id' in params: params.pop('id')
        else:
            pk = params.pop('id')
        return (pk, params)

    def with_datetimes(self, params):
        if isinstance(params, dict):
            params.update({ 'updated_at': timezone.now() })
        return params

    def build_query_set(self, queryset, **filters):
        for key in filters:
            if key in self._allowed_filters:
                value = filters[key]
                key = self._allowed_filters[key]
                if isinstance(value, str):
                    value = f"'{value}'"
                elif isinstance(value, list) or isinstance(value, tuple):
                    values = []
                    for v in value: values.append(f"'{v}'")
                    value = ','.join(values)
                queryset = eval(f"queryset.{key}({value})")
        return queryset

    @property
    def _allowed_filters():
        """ Mapping keys to filters of model """
        return {
            'orderby': 'order_by',
            'order_by': 'order_by',
            'only': 'only',
            'defer': 'defer',
        }
