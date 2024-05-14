import os
import asyncio
from app.models import novels
from app.scrapper.elementextractor import element_extractor
from app.scrapper.scrappy import create_connection
import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import text

# TODO IMAGE EXTRACTOR AND USING COLUMN TO TRACK INSTREAD
custom_filename = ""
stop_flag = False 

async def load_processed_filenames(filename):
    filenames = set()
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                filenames.add(line.strip())
    return 

# async def load_processed_filenames(session):
#     filenames = set()
#     # Assuming `session` is a SQLAlchemy session object
#     results = session.query(novels.title).all()
#     for result in results:
#         filenames.add(result.column_name.strip())
#     return filenames


async def scrape_novel(session, url, processed_filenames, filename, txtdirectory):
    try:
        with open(os.path.join(txtdirectory,f"{filename}.txt"), 'r') as file:
            last_processed_chapter = int(file.read())
    except FileNotFoundError:
        last_processed_chapter = 0

    chapter_number = last_processed_chapter + 1 
    while True:
        if stop_flag:
            break
        base_url = f"{url}chapter-{chapter_number}/"
        async with session.get(base_url) as response:
            if response.status != 200:
                print(f"Chapter {chapter_number} not found. Exiting...")
                break
            else:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                title, content = await extract_content(soup)
                if title is None and content is None:
                    end_url = f"{base_url}-end"
                    async with session.get(end_url) as end_response:
                        if end_response.status == 200:
                            soup = BeautifulSoup(await end_response.text(), 'html.parser')
                            title, content = await extract_content(soup)
                            if title is None and content is None:
                                print("No more chapters found. Exiting...")
                                break
                        else:
                            print("No more chapters found. Exiting...")
                            break
                yield title, content
                processed_filenames.add(title)
                # Create directories if they don't exist
                os.makedirs(os.path.dirname(os.path.join(txtdirectory, f"{filename}.txt")), exist_ok=True)

                with open(os.path.join(txtdirectory, f"{filename}.txt"), 'w') as file:
                    file.write(str(chapter_number)) 

                chapter_number += 1


async def extract_content(soup):
    title, content = element_extractor(soup)
    return title, content

async def insert_novel(conn, novel_title, genre):
    try:
        existing_novel_query = text(f"SELECT novel_id FROM novels WHERE title = :title;")
        result = conn.execute(existing_novel_query, {"title": novel_title})
        existing_novel = result.fetchone()
        if existing_novel:
            print(f"Novel '{novel_title}' already exists. Skipping insertion.")
            return
        conn.execute(
            text(f"INSERT INTO novels (title, genre) VALUES (:novel_title, :genre);"),
            {"novel_title": novel_title, 'genre': genre}
        )
        print(f"Novel '{novel_title}' inserted into novels table.")
    except Exception as e:
        print("Error inserting novel data:", e)

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
    
async def save_to_database(conn, novel_id,chapter_title, chapter_content):
        conn.execute(
            text(f"INSERT INTO chapters (novel_id, title, content) VALUES (:novel_id, :chapter_title, :chapter_content);"),
            {"novel_id": novel_id, "chapter_title": chapter_title, "chapter_content": chapter_content}
        )
        print(f"Chapter '{chapter_title}' inserted into chapters table.")


async def crawl_page(session, base_url, page_number, processed_filenames, txtdirectory, genre):
    global stop_flag
    if stop_flag:
        return False
    url = f"{base_url}{page_number}/"
    print(url)
    async with session.get(url) as response:
        if response.status == 404:
            print("404 Not Found. No more pages to crawl. Exiting...")
            # stop_flag = True
            return True  
        if response.status != 200:
            print(f"Page {page_number} not found. Exiting...")
            return False
        page_source = await response.text()
        soup = BeautifulSoup(page_source, 'html.parser')
        filtered_links = [link for link in soup.find_all('a') if link.get('href', '').startswith("https://boxnovel.com/novel/") 
                        and "/novel/page/" not in link.get('href', '') 
                        and "chapter" not in link.get('href', '').lower()
                        and len(link.get('href', '').split('/novel/')[1]) > 0]
        unique_links = set()
        for link in filtered_links:
            text = link.get_text(strip=True)
            url = link.get('href')
            if text and url:
                filename = f"{text.replace(' ', '')}"
                novel_title = text
                if filename in processed_filenames:
                    print("Skipping duplicate. Title and filename already saved.")
                    continue
                if text in unique_links:
                    print("Skipping duplicate title:", text)
                    continue
                unique_links.add(text)
                processed_filenames.add(filename)
                conn = create_connection()
                insert_novel(conn, novel_title, genre)
                async for title_, content in scrape_novel(session, url, processed_filenames, custom_filename, txtdirectory):
                    # await create_csv(filename, directory)
                    novel_id = await fetch_novel_id(conn, novel_title)
                    await save_to_database(conn, novel_id, title_, content)
    
    return False                    

async def crawl_webpage(base_url, genre, start_page=1):
    global stop_flag
    global custom_filename

    genre = [1,2,3,4,5,6]
    processed_filenames = await load_processed_filenames(custom_filename)
    root_work_dirs = "/home/dexter/Desktop/scrape"
    txtdirectory = os.path.join(root_work_dirs, f'txtdirs/{genre.lower()}')
    async with aiohttp.ClientSession() as session:
        page_number = start_page
        while True:
                if await crawl_page(session, base_url, page_number, processed_filenames, txtdirectory, genre):        
                    break
                page_number += 1
            

async def main():
    global custom_filename
    genres = ["action","comedy", "adventure", "drama", "eastern", "fantasy", "harem"]
    start_index = genres.index("action") 
    for genre in genres[start_index:]:
        base_url = f"https://boxnovel.com/manga-genre/{genre}/page/"
        print(f"Crawling genre: {genre}")
        await crawl_webpage(base_url, genre, start_page=1)
   
        start_index += 1
if __name__ == "__main__":
    asyncio.run(main())