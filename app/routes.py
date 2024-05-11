from flask import Blueprint, jsonify, request
from app.models import novels, chapters
from app.pagination import paginate_query
from app.views import serialize_chapters, serialize_novels

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

@routes.route('/get-chapters/<int:novel_id>', methods=['GET'])
def get_chapters(novel_id):
    page_number = request.args.get('page', 1, type=int)
    pagination = paginate_query(chapters.query.filter_by(novel_id=novel_id), page_number)
    serialized_chapters = serialize_chapters(pagination.items)

            # params is page i dont know why the fuck it was not current_page
            # sample http://localhost:5000/get-chapters/100?page=1

    return jsonify({
        'chapters': serialized_chapters,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'total_items': pagination.total
    })

