import re
from bs4 import BeautifulSoup

async def scrape_summary(session, url):
    async with session.get(url) as response:
        response_content = await response.text()
        soup = BeautifulSoup(response_content, 'html.parser')
        summary_text = []

        if soup.find(class_='summary__content'):
            summary_content_elements = soup.find_all(class_='summary__content')
            
            for element in summary_content_elements:
                for p in element.find_all('p'):
                    if not p.find_all(recursive=False):
                        text_content = p.get_text(strip=True)
                        if not re.fullmatch(r'_+', text_content):
                            summary_text.append(p.get_text(strip=True))


        if soup.find(class_='c_000'):
            summary_content_elements = soup.find_all(class_='summary__content')
            for element in summary_content_elements:
                c_000_elements = element.find_all(class_='c_000')
                for c_000_element in c_000_elements:
                    for div in c_000_element.find_all('div'):
                        div.decompose()

            for element in summary_content_elements:
                text_without_boxnovel = re.sub(r'ƁΟXNƟVEL\.CʘM', '', element.get_text(strip=True))
                summary_text.append(text_without_boxnovel)
                print(text_without_boxnovel)


        return '\n'.join(summary_text)
            


