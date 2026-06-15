from bs4 import BeautifulSoup
import asyncio
import aiohttp

async def get_img_data(session, url):
    headers = {'User-Agent': 'MyLearningScraper/1.0 (contact@example.com)'}
    async with session.get(url, headers=headers) as res:
        res.raise_for_status() # Raise an exception for bad status codes like 403 or 404
        return await res.read()

async def get_img_urls(session, url):
    headers = {'User-Agent': 'MyLearningScraper/1.0 (contact@example.com)'}
    async with session.get(url, headers=headers) as res:
        html = await res.text()
        soup = BeautifulSoup(html, 'html.parser')
        # img_tags = soup.find_all('img')
        return [img.get('src') for img in soup.find_all('img')]



async def main():
    async with aiohttp.ClientSession() as sesh:
        urls = await get_img_urls(sesh, 'https://en.wikipedia.org/wiki/Cold_War')
        tasks = [ asyncio.create_task(get_img_data(sesh, url)) for url in urls]
        results = asyncio.gather(*tasks)



if __name__ == '__main__':
    asyncio.run(main())
