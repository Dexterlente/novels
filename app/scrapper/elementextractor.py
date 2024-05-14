async def element_extractor(soup):   
    title, content = None, None
    if soup.find(class_='cha-tit'):  # Check if the page structure matches the first website
        title_div = soup.find(class_='cha-tit')
        title_text = title_div.find('h3').get_text(strip=True) if title_div.find('h3') else \
                title_div.find('h1').get_text(strip=True) if title_div.find('h1') else ""
        title_p_text = title_div.find('p').get_text(strip=True) if title_div.find('p') else ""
        title = f"{title_text}\n{title_p_text}"

        content_body = soup.find_all(class_='cha-content')
        content = "\n".join([element.get_text(strip=True) for element in content_body]) if content_body else "Content not found"

    elif soup.find(class_='text-center'):
        title_element = soup.find(class_='text-center')
        title = title_element.get_text(strip=True)
        parent_element = title_element.parent
        if parent_element:
            for div_element in parent_element.find_all('div'):
                div_element.decompose()               
            content = parent_element.get_text(separator='\n', strip=True)

        else:
            content = "Content not found"

    elif soup.find(class_='text-left'):  # Check if the page structure matches the second website
        chapter_contents = soup.find_all(class_='text-left')
        for post in chapter_contents:
            for div in post.find_all('div'):
                div.decompose()
        if chapter_contents:
            first_post = chapter_contents[0]
            first_element = first_post.find_next()
            if first_element:
                title = first_element.get_text(strip=True)
                content = "\n".join([content.get_text(strip=True) for content in chapter_contents])
    print(title)
    return title, content
