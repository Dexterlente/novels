from sqlalchemy import text


async def increment_last_chapter(conn, novel_title):
    conn.execute(text(f"UPDATE novels SET last_chapter = last_chapter + 1 WHERE title = '{novel_title}';"))
    print("increment")