import os
import asyncio
from app.models import novels
from app.scrapper.dbinsertion import insert_chapters_logic, novel_insertion_logic
from app.scrapper.elementextractor import element_extractor
from app.scrapper.scrappy import create_connection
import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import text

# TODO IMAGE EXTRACTOR AND USING COLUMN TO TRACK INSTREAD

# TODO FOR TEST
async def novel_tracker(conn, novel_title):
    try:
        result = conn.execute(
                text(f"SELECT *
                        FROM novels
                        WHERE title IS NULL OR title = '{novel_title}'
                        OR last_chapter IS NULL OR last_chapter = 0;"))
        row = result.fetchone()
        if row:
            last_chapter = row[0]
            if last_chapter is not None:
                return last_chapter  
            else:
                return 0 
        else:
            return 0
    except Exception as e:
        print("Error executing query:", e)
        return None 

async def scrape_novel(session, url, novel_title):
    # try:
    #     with open(os.path.join(txtdirectory,f"{filename}.txt"), 'r') as file:
    #         last_processed_chapter = int(file.read())
    # except FileNotFoundError:
    #     last_processed_chapter = 0

    chapter_number = last_processed_chapter + 1 
    while True:
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
                # Create directories if they don't exist
                # os.makedirs(os.path.dirname(os.path.join(txtdirectory, f"{filename}.txt")), exist_ok=True)

                # with open(os.path.join(txtdirectory, f"{filename}.txt"), 'w') as file:
                #     file.write(str(chapter_number)) 

                # chapter_number += 1


async def extract_content(soup):
    title, content = element_extractor(soup)
    return title, content

async def insert_novel(conn, novel_title, genre_int):
    novel_insertion_logic(conn, novel_title, genre_int)
    print("novel insert sucess")

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
    
async def insert_chapters(conn, novel_id, chapter_title, chapter_content):
    insert_chapters_logic(conn, novel_id, chapter_title, chapter_content)
    print("Inserted chapters")


async def crawl_page(session, base_url, page_number, genre_int):
    url = f"{base_url}{page_number}/"
    print(url)
    async with session.get(url) as response:
        if response.status == 404:
            print("404 Not Found. No more pages to crawl. Exiting...")
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
                if text in unique_links:
                    print("Skipping duplicate title:", text)
                    continue
                unique_links.add(text)
                conn = create_connection()
                insert_novel(conn, novel_title, genre_int)
                async for title, content in scrape_novel(session, url, novel_title):
                    novel_id = await fetch_novel_id(conn, novel_title)
                    await insert_chapters(conn, novel_id, title, content)
    
async def crawl_webpage(base_url, genre_int, start_page=1):

    async with aiohttp.ClientSession() as session:
        page_number = start_page
        while True:
                if await crawl_page(session, base_url, page_number, genre_int):        
                    break
                page_number += 1
            

async def main():
    genre_mapping = {
        "action": 1,
        "comedy": 2,
        "adventure": 3,
        "drama": 4,
        "eastern": 5,
        "fantasy": 6,
        "harem": 7
    }
    genres = ["action","comedy", "adventure", "drama", "eastern", "fantasy", "harem"]
    start_index = genres.index("action") 
    for genre in genres[start_index:]:
        genre_int = genre_mapping.get(genre)
        base_url = f"https://boxnovel.com/manga-genre/{genre}/page/"
        print(f"Crawling genre: {genre}")
        await crawl_webpage(base_url, genre_int)
   
        start_index += 1
if __name__ == "__main__":
    asyncio.run(main())