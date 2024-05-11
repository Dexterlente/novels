
def serialize_novels(novels_list):
    """
    Serialize a list of novel objects into a list of dictionary representations.
    """
    serialized_novels = []
    for novel in novels_list:

        serialized_novel = {
            'novel_id': novel.novel_id,
            'image_url': novel.image_url,
            'title': novel.title,
            'genre': novel.genre,
            'novel_title': novel.novel_new_title,
        }
        serialized_novels.append(serialized_novel)
    return serialized_novels



def serialize_chapters(chapters_list, novel_id=None):
    """
    Serialize a list of chapters objects into a list of dictionary representations.
    If novel_id is provided, only chapters belonging to that novel will be included.
    """
    serialized_chapters = []
    chapter_numbers = {}
    
    for chapter in chapters_list:
        if novel_id is not None and chapter.novel_id != novel_id:
            continue

        if chapter.novel_id not in chapter_numbers:
            # Initialize chapter_number for a novel_id if it's not present
            chapter_numbers[chapter.novel_id] = 1

        # Assign chapter_number from the dictionary
        chapter_number = chapter_numbers[chapter.novel_id]

        # Update chapter_number for the next chapter
        chapter_numbers[chapter.novel_id] += 1

        serialized_chapter = {
            'chapter_id': chapter.chapter_id,
            'novel_id': chapter.novel_id,
            'timestamp': chapter.timestamp,
            'chapter_number': chapter_number
        }
        serialized_chapters.append(serialized_chapter)

    return serialized_chapters

