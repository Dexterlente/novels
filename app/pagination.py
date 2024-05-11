
def paginate_query(query, page_number=1, per_page=10):
    """
    Paginate a query and return a Pagination object.
    """
    return query.paginate(page=page_number, per_page=per_page, error_out=False)