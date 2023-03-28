def queryParser(self):
    query = self.request.GET.get('query')
    order_by = self.request.GET.get('order_by')
    value = self.request.GET.get('value')
    if order_by is None or order_by == '':
        order_by = 'name'
    if value is None or value == '':
        value = 'asc'
    if value == 'desc':
        order_by = '-' + order_by
    return query, order_by, value
