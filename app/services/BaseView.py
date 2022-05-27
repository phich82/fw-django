class BaseView:

    def _resolve_query_string(self, request, field='updated_at'):
        order_by_field = request.GET.get('order_by', field)
        direction = request.GET.get('direction', 'desc')
        order_by = order_by_field
        if direction == 'desc':
            order_by = f"-{order_by}"

        return (direction, order_by_field, order_by)
