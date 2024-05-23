from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


"""
 WITH chapters_to_delete AS (
    SELECT novel_id, chapter_id
    FROM (
        SELECT novel_id, chapter_id,
               ROW_NUMBER() OVER (PARTITION BY novel_id ORDER BY chapter_id DESC) AS row_num
        FROM chapters
    ) AS numbered_chapters
    WHERE row_num <= 10
)
DELETE FROM chapters
WHERE (novel_id, chapter_id) IN (SELECT novel_id, chapter_id FROM chapters_to_delete);
"""