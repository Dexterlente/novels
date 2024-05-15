async def increment_last_chapter(conn):
    conn.execute(f"UPDATE novels
        SET last_chapter = last_chapter + 1
        WHERE title = 'Title of the Novel';
        ")