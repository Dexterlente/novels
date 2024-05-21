   
from flask import request
from app.database import db

from app.models import chapters, novels
from app.pagination import paginate_query
from app.serializer import serialize_chapter_detail, serialize_chapters, serialize_novels, serialize_novels_genre, serialized_novels_detail


def get_novels_logic():
    page_number = request.args.get('page', 1, type=int)
    pagination = paginate_query(novels.query, page_number)
    serialized_novels = serialize_novels(pagination.items)

    return {
        'novels': serialized_novels, 
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'total_items': pagination.total
    }

def get_novels_by_genre_logic(genre):
    page_number = request.args.get('page', 1, type=int)
    pagination = paginate_query(novels.query.filter_by(genre=genre), page_number)

    serialized_novels = serialize_novels_genre(pagination.items)
    return {
        'novels': serialized_novels, 
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'total_items': pagination.total
    }

def get_random_novels_by_genre_logic(genre):
    
    random_novels = novels.query.filter_by(genre=genre).order_by(db.func.random()).limit(7).all()
    serialized_novels = serialize_novels_genre(random_novels)
    
    return serialized_novels

def get_novels_by_details_logic(novel_id):
    novel = novels.query.filter_by(novel_id=novel_id).first()
    if novel:
        serialized_novel = serialized_novels_detail(novel)
        return serialized_novel
    else:
         return {'error': 'novel not found'}, 404


def get_chapters_logic(novel_id):
    page_number = request.args.get('page', 1, type=int)
    per_page = 50
    pagination = paginate_query(chapters.query.filter_by(novel_id=novel_id), page_number, per_page)
    serialized_chapters = serialize_chapters(pagination.items)

    return {
        'chapters': serialized_chapters,
        'total_pages': pagination.pages,
        'current_page': pagination.page,
        'total_items': pagination.total
    }

def get_chapter_details_logic(novel_id, chapter_id):
    chapter = chapters.query.filter_by(novel_id=novel_id, chapter_id=chapter_id).first()
    if chapter:
        serialized_chapter = serialize_chapter_detail(chapter)
        return serialized_chapter
    else:
         return {'error': 'Chapter not found'}, 404
