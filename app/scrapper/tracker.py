from sqlalchemy import text


async def novel_tracker(conn, novel_title):
    try:
        result = conn.execute(
                text(f"SELECT last_chapter
                      FROM novels
                      WHERE title = '{novel_title}';"))
        row = result.fetchone()
        if row:
            last_chapter = row[0]
            if last_chapter is not None:
                return last_chapter  
        return 0
    except Exception as e:
        print("Error executing query:", e)
        return None