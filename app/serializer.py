
from app.models import chapters


def process_image_url(url):
        if url.endswith("-110x150.jpg"):
            return url.replace("-110x150.jpg", ".jpg")
        elif url.endswith("-110x150.jpeg"):
            return url.replace("-110x150.jpeg", ".jpeg")
        return url

def serialize_novels(novels_list):
    """
    Serialize a list of novel objects into a list of dictionary representations.
    """
    serialized_novels = []

    for novel in novels_list:
        processed_image_url = process_image_url(novel.image_url)

        serialized_novel = {
            'novel_id': novel.novel_id,
            'image_url': novel.image_url,
            'image_url_cover': processed_image_url,
            'title': novel.title,
            'genre': novel.genre,
        }
        serialized_novels.append(serialized_novel)
    return serialized_novels

def serialize_novels_genre(novel_list_genre):

    serialize_novels_genres = []

    for novels in novel_list_genre:
        processed_image_url = process_image_url(novels.image_url)

        serialize_novels_genre = {
            'novel_id': novels.novel_id,
            'image_url': novels.image_url,
            'image_url_cover': processed_image_url,
            'title': novels.title,
            'genre': novels.genre,
            'synopsis': novels.synopsis,
        }
        serialize_novels_genres.append(serialize_novels_genre)
    return serialize_novels_genres

def serialize_novels_genre_random(novel_list_genre):

    serialize_novels_genres = []

    for novels in novel_list_genre:
        processed_image_url = process_image_url(novels.image_url)

        serialize_novels_genre = {
            'novel_id': novels.novel_id,
            'image_url': novels.image_url,
            'image_url_cover': processed_image_url,
            'title': novels.title,
            'genre': novels.genre,
            'synopsis': novels.synopsis,
        }
        serialize_novels_genres.append(serialize_novels_genre)
    return serialize_novels_genres

def serialized_novels_detail(novel, novel_id=None):

    processed_image_url = process_image_url(novel.image_url)
    serialized_novel = {
        'novel_id': novel.novel_id,
        'image_url_cover': processed_image_url,
        'title': novel.title,
        'genre': novel.genre,
        'synopsis': novel.synopsis,
    }

    return serialized_novel



def serialize_chapters(chapters_list, novel_id=None):
    """
    Serialize a list of chapters objects into a list of dictionary representations.
    If novel_id is provided, only chapters belonging to that novel will be included.
    """
    serialized_chapters = []

    
    for chapter in chapters_list:
        if novel_id is not None and chapter.novel_id != novel_id:
            continue


        serialized_chapter = {
            'chapter_id': chapter.chapter_id,
            'novel_id': chapter.novel_id,
            'timestamp': chapter.timestamp,
            'chapter_number': chapter.index
        }
        serialized_chapters.append(serialized_chapter)

    return serialized_chapters

def serialize_chapter_detail(chapter, novel_id=None, chapter_id=None):
    """
    Serialize details of a specific chapter into a dictionary representation.
    If novel_id and chapter_id are provided, filter the chapter based on these parameters.
    """
    if novel_id is not None and chapter.novel_id != novel_id:
        return None  # Chapter does not belong to the specified novel

    if chapter_id is not None and chapter.chapter_id != chapter_id:
        return None  # Chapter does not have the specified chapter_id
    
    next_chapter = chapters.query.filter_by(novel_id=novel_id, index=chapter.index + 1).first()
    if next_chapter:
        print(f"Next chapter found: {next_chapter.chapter_id}")
    else:
        print("No next chapter found")

    # Fetch the previous chapter based on the index
    previous_chapter = chapters.query.filter_by(novel_id=novel_id, index=chapter.index - 1).first()
    if previous_chapter:
        print(f"Previous chapter found: {previous_chapter.chapter_id}")
    else:
        print("No previous chapter found")

    print(novel_id, chapter_id, "sdads")
    serialized_chapter = {
        'chapter_id': chapter.chapter_id,
        'novel_id': chapter.novel_id,
        'timestamp': chapter.timestamp,
        'title': chapter.title,
        'content': chapter.content,
        'index': chapter.index,
        'next_chapter_id': next_chapter.chapter_id if next_chapter else None,
        'previous_chapter_id': previous_chapter.chapter_id if previous_chapter else None
    }

    return serialized_chapter

def serialize_chapters_update_list(chapters_list):
    """
    Serialize a list of chapters objects into a list of dictionary representations.
    all latest chapters on the chapter db is rendered here
    """
    serialized_chapters = []
    
    for chapter in chapters_list:

        serialized_chapter = {
            'chapter_id': chapter.chapter_id,
            'novel_id': chapter.novel_id,
            'novel_title': chapter.novel.title,
            'chapter_title': chapter.title,
            'chapter_number': chapter.index,
            'timestamp': chapter.timestamp,
        }
        serialized_chapters.append(serialized_chapter)

    return serialized_chapters


def serialized_novels_search(query):
    serialized_novels = []
    for q in query:
        processed_image_url = process_image_url(q.image_url)
        serialized_novel = {
            'novel_id': q.novel_id,
            'image_url_cover': processed_image_url,
            'title': q.title,
            'genre': q.genre,
            'synopsis': q.synopsis,
        }
        serialized_novels.append(serialized_novel)

    return serialized_novels