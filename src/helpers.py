from bs4 import BeautifulSoup
import asyncio
import aiohttp
from urllib.parse import urljoin

async def get_img_data(session, url):
    headers = {'User-Agent': 'MyLearningScraper/1.0 (contact@example.com)'}
    async with session.get(url, headers=headers) as res:
        res.raise_for_status() # Raise an exception for bad status codes like 403 or 404
        return await res.read()

async def get_img_urls(session, base_url):
    headers = {'User-Agent': 'MyLearningScraper/1.0 (contact@example.com)'}
    async with session.get(base_url, headers=headers) as res:
        html = await res.text()
        soup = BeautifulSoup(html, 'html.parser')
        
        results = []
        for img in soup.find_all('img'):
            src = img.get('src')
            if not src: continue
            
            # Clean up URLs (resolve relative urls like //upload.wikimedia...)
            u = urljoin(base_url, src)
            
            # Filter out SVGs as Pillow does not natively support them
            if u.lower().endswith('.svg'):
                continue
            
            # Try to get alt text, fallback to filename from URL
            alt = img.get('alt')
            if not alt or not alt.strip():
                alt = u.split('/')[-1]
                
            results.append({'url': u, 'name': alt})
            
        return results



async def main():
    async with aiohttp.ClientSession() as sesh:
        urls = await get_img_urls(sesh, 'https://en.wikipedia.org/wiki/Cold_War')
        tasks = [ asyncio.create_task(get_img_data(sesh, url)) for url in urls]
        results = asyncio.gather(*tasks)



if __name__ == '__main__':
    asyncio.run(main())
