from sqlalchemy import text

async def novel_insertion_logic(conn, novel_title, genre_int):   
    try:
        existing_novel_query = text(f"SELECT novel_id FROM novels WHERE title = :title;")
        result = conn.execute(existing_novel_query, {"title": novel_title})
        existing_novel = result.fetchone()
        if existing_novel:
            print(f"Novel '{novel_title}' already exists. Skipping insertion.")
            return
        conn.execute(
            text(f"INSERT INTO novels (title, genre) VALUES (:novel_title, :genre);"),
            {"novel_title": novel_title, 'genre': genre_int}
        )
        print(f"Novel '{novel_title}' inserted into novels table.")
    except Exception as e:
        print("Error inserting novel data:", e)

async def insert_chapters(conn, novel_id,chapter_title, chapter_content):
        conn.execute(
            text(f"INSERT INTO chapters (novel_id, title, content) VALUES (:novel_id, :chapter_title, :chapter_content);"),
            {"novel_id": novel_id, "chapter_title": chapter_title, "chapter_content": chapter_content}
        )
        print(f"Chapter '{chapter_title}' inserted into chapters table.")