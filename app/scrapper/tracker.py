from sqlalchemy import text


async def novel_tracker(conn, novel_title):
    try:
        result = conn.execute(
                text(f"SELECT last_chapter FROM novels WHERE title = '{novel_title}';"))
        row = result.fetchone()
        return row[0] if row else 0
    except Exception as e:
        print("Error executing query:", e)
        return None