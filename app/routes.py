import asyncio
from flask import Blueprint, jsonify, request
from app.logic.utils import get_chapter_details_logic, get_chapters_logic, get_novels_by_genre_logic, get_novels_logic
from app.pagination import paginate_query
from app.scrapper.scrappy import main
from app.serializer import serialize_chapter_detail, serialize_chapters, serialize_novels, serialize_novels_genre

routes = Blueprint('views', __name__)

@routes.route('/get-novels')
def get_novels():
    result = get_novels_logic()
    return jsonify(result)

@routes.route('/get-novels/<int:genre>', methods=['GET'])
def get_novels_by_genre(genre):
    result = get_novels_by_genre_logic(genre)
    return jsonify(result)

@routes.route('/get-chapters/<int:novel_id>', methods=['GET'])
def get_chapters(novel_id):
    result = get_chapters_logic(novel_id)
    return jsonify(result)

@routes.route('/get-chapters/<int:novel_id>/<int:chapter_id>', methods=['GET'])
def get_chapter_details(novel_id, chapter_id):
    result = get_chapter_details_logic(novel_id, chapter_id)
    return jsonify(result)

@routes.route('/start-scraping')
def start_scraping():
    asyncio.run(main())
    return 'Scraping process initiated.'