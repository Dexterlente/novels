from sqlalchemy import text

async def novel_insertion_logic(conn, novel_title, genre_int, image_url):   
    try:
        existing_novel_query = text(f"SELECT novel_id FROM novels WHERE title = :title;")
        result = conn.execute(existing_novel_query, {"title": novel_title})
        existing_novel = result.fetchone()
        if existing_novel:
            print(f"Novel '{novel_title}' already exists. Skipping insertion.")
            return
        conn.execute(
            text(f"INSERT INTO novels (title, genre, image_url) VALUES (:novel_title, :genre, :image_url);"),
            {"novel_title": novel_title, 'genre': genre_int, 'image_url': image_url}
        )
        print(f"Novel '{novel_title}' inserted into novels table.")
    except Exception as e:
        print("Error inserting novel data:", e)

async def insert_chapters(conn, novel_id,chapter_title, chapter_content):
    # wards
    try:
        existing_chapter_query = text(f"SELECT novel_id FROM chapters WHERE title = :chapter_title;")
        result = conn.execute(existing_chapter_query, {"novel_id": novel_id, "chapter_title": chapter_title})
        existing_chapter = result.fetchone()

        if existing_chapter:
            print(f"Chapter '{chapter_title}' already exists in chapters table.")
            return
        
        last_chapter_query = text("SELECT last_chapter FROM novels WHERE novel_id = :novel_id")
        last_chapter = conn.execute(last_chapter_query, {"novel_id": novel_id}).fetchone()[0]

        if last_chapter is None:
            new_index = 1
        else:
            new_index = last_chapter
            print(f"new chapter number {new_index}")
            conn.execute(
                text(f"INSERT INTO chapters (novel_id, title, content, index) VALUES (:novel_id, :chapter_title, :chapter_content, :index);"),
                {"novel_id": novel_id, "chapter_title": chapter_title, "chapter_content": chapter_content, "index": new_index}
            )
            print(f"Chapter '{chapter_title}' inserted into chapters table.")
    except Exception as e:
        print("Error inserting chapter data:", e)

async def fetch_novel_id(conn, novel_title):
    try:
        novel_id_query = text("SELECT novel_id FROM novels WHERE title = :title;")
        result = conn.execute(novel_id_query, {"title": novel_title})
        row = result.fetchone()
        if row:
            return row[0]
        else:
            return None
    except Exception as e:
        print("Error fetching novel data:", e)
        return None

async def insert_synopsis(conn, synopsis, novel_title):
        synopsis_query = text("SELECT title FROM novels WHERE synopsis IS NULL;")
        result = conn.execute(synopsis_query, {"title": novel_title})
        nulledSynopsis = result.fetchone()

        if nulledSynopsis:
            conn.execute(
                text(f"UPDATE novels SET synopsis = :synopsis WHERE title = :novel_title AND synopsis IS NULL;"),
                {"synopsis": synopsis, "novel_title": novel_title}
            )
            print("Synopsis inserted Sucessfully")
        else:
            print('already have synopsis')
            return