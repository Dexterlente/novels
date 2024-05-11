from flask import Blueprint, jsonify, request
from app.models import novels, chapters
from app.pagination import paginate_query
from app.views import serialize_novels

routes = Blueprint('views', __name__)

@routes.route('/get-novels')
def get_novels():
    page_number = request.args.get('page', 1, type=int)
    pagination = paginate_query(novels.query, page_number)
    serialized_novels = serialize_novels(pagination.items)

    return jsonify({
        'novels': serialized_novels,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'total_items': pagination.total
    })

