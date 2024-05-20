import asyncio
from app.scrapper.dbinsertion import fetch_novel_id, insert_chapters, novel_insertion_logic
from app.scrapper.elementextractor import element_extractor
from app.scrapper.extracsynosis import scrape_summary
from app.scrapper.incrementquery import increment_last_chapter
from app.scrapper.dbconnection import create_connection
import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy import text

from app.scrapper.tracker import novel_tracker

async def scrape_novel(session, url, novel_title, conn, genre_int, image_url):
    last_chapter = await novel_tracker(conn, novel_title)
    synopsis = await scrape_summary(session, url)
    print("ss",synopsis, "")
#   TODO insertion 

    chapter_number = (last_chapter or 0) + 1 
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

                if title is None:
                    await insert_novel(conn, novel_title, genre_int, image_url)

                await increment_last_chapter(conn, novel_title)
                
                chapter_number += 1

async def extract_content(soup):
    title, content = await element_extractor(soup)
    return title, content

async def insert_novel(conn, novel_title, genre_int, image_url):
    await novel_insertion_logic(conn, novel_title, genre_int, image_url)
    conn.commit()


async def crawl_page(session, base_url, page_number, genre_int):
    url = f"{base_url}{page_number}/"
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
            img_tag = link.find('img')
            if img_tag:
                image_url = img_tag['data-src']
            text = link.get_text(strip=True)
            url = link.get('href')
            if text and url:
                novel_title = text
                if text in unique_links:
                    print("Skipping duplicate title:", text)
                    continue
                unique_links.add(text)
                engine, conn = create_connection()
                await insert_novel(conn, novel_title, genre_int , image_url)
                conn.commit()

                async for title, content in scrape_novel(session, url, novel_title, conn ,genre_int, image_url):
                    novel_id = await fetch_novel_id(conn, novel_title)
                    await insert_chapters(conn, novel_id, title, content)
                    conn.commit()
                conn.close()
    
async def crawl_webpage(base_url, genre_int, start_page=1):

    async with aiohttp.ClientSession() as session:
        page_number = start_page
        visited_pages = set()
        while True:
            if page_number in visited_pages:
                break
            visited_pages.add(page_number)
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
    start_index = genres.index("comedy") 
    for genre in genres[start_index:]:
        genre_int = genre_mapping.get(genre)
        base_url = f"https://boxnovel.com/manga-genre/{genre}/page/"
        print(f"Crawling genre: {genre}")
        try:
            await crawl_webpage(base_url, genre_int)
        except Exception as e:
            print(f"An error occurred while crawling {genre}: {e}")

if __name__ == "__main__":
    asyncio.run(main())



    # // Override the debugger function to prevent it from stopping execution
        # window.debugger = function() {};