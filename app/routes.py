import asyncio
from flask import Blueprint, jsonify, request
from app.logic.utils import get_chapter_details_logic, get_chapters_logic, get_latest_chapters_logic, get_novel_search_details_logic, get_novel_search_logic, get_novels_by_details_logic, get_novels_by_genre_logic, get_novels_logic, get_random_novels_by_genre_logic, get_single_random_novel_by_genre_logic
from app.pagination import paginate_query
from app.scrapper.scrappy import main

routes = Blueprint('views', __name__)

@routes.route('/get-novels')
def get_novels():
    result = get_novels_logic()
    return jsonify(result)

@routes.route('/get-novels/<int:genre>', methods=['GET'])
def get_novels_by_genre(genre):
    result = get_novels_by_genre_logic(genre)
    return jsonify(result)

@routes.route('/get-single-novel-random/<int:genre>', methods=['GET'])
def get_single_novel_random_genre(genre):
    result = get_single_random_novel_by_genre_logic(genre)
    return jsonify(result)

@routes.route('/get-novels-random/<int:genre>', methods=['GET'])
def get_novels_by_random_genre(genre):
    result = get_random_novels_by_genre_logic(genre)
    return jsonify(result)

@routes.route('/get-novel-details/<int:novel_id>', methods=['GET'])
def get_novels_novel(novel_id):
    result = get_novels_by_details_logic(novel_id)
    return jsonify(result)

@routes.route('/get-chapters/<int:novel_id>', methods=['GET'])
def get_chapters(novel_id):
    result = get_chapters_logic(novel_id)
    return jsonify(result)

@routes.route('/get-chapters/<int:novel_id>/<int:chapter_id>', methods=['GET'])
def get_chapter_details(novel_id, chapter_id):
    result = get_chapter_details_logic(novel_id, chapter_id)
    return jsonify(result)

@routes.route('/get-latest-chapters', methods=['GET'])
def get_latest_chapters():
    result = get_latest_chapters_logic()
    return jsonify(result)

@routes.route('/search', methods=['GET'])
def get_novel_search():
    query = request.args.get('query', '') 
    result = get_novel_search_logic(query)
    return jsonify(result)

@routes.route('/search/details/<int:novel_id>', methods=['GET'])
def get_novel_search_detail(novel_id):
    result = get_novel_search_details_logic(novel_id)
    return jsonify(result)

@routes.route('/start-scraping')
def start_scraping():
    asyncio.run(main())
    return 'Scraping process initiated.'


# -- Update the index values
# UPDATE chapters c
# SET index = subquery.row_num
# FROM (
#     SELECT chapter_id, 
#            ROW_NUMBER() OVER (PARTITION BY novel_id ORDER BY timestamp) AS row_num
#     FROM chapters
# ) AS subquery
# WHERE c.chapter_id = subquery.chapter_id;



# TODO 
# WITH duplicates AS (
#     SELECT 
#         chapter_id,
#         ROW_NUMBER() OVER (PARTITION BY novel_id, title ORDER BY chapter_id) AS row_num
#     FROM 
#         chapters
# )
# DELETE FROM chapters
# WHERE (novel_id, title) IN (
#     SELECT 
#         novel_id,
#         title
#     FROM 
#         duplicates
#     WHERE 
#         title IS NOT NULL
#         AND row_num > 1
# );
