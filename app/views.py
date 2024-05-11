
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
        }
        serialized_novels.append(serialized_novel)
    return serialized_novels
