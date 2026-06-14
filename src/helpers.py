from bs4 import BeautifulSoup
import asyncio
import aiohttp

async def fetch_img_urls(session, url):
    async with session.get(url) as res:
        html = await res.text()
        soup = BeautifulSoup(html, 'html.parser')
        return [img.get('src') for img in soup.find_all('img') if img.get('src')]
    
async def fetch_img(session, url):
    async with session.get(url) as res:
        data = await res.read()
        return {'url': url, 'data': data }

# async with aiohttp.ClientSession() as s:

# async def download_and_save_image(session, img_url):
#     async with session.get(img_url) as res:
#         data = await res.read()
#         async with aiofiles.open(f'{DOWNLOAD_FOLDER}/{img_url}', mode='wb') as f:
#             await f.write(data)

async def get_img_urls(session, url):
    headers = {'User-Agent': 'MyLearningScraper/1.0 (contact@example.com)'}
    async with session.get(url, headers=headers) as res:
        html = await res.text()
        soup = BeautifulSoup(html, 'html.parser')
        img_tags = soup.find_all('img')
        return [img.get('src') for img in img_tags]

async def main():
    async with aiohttp.ClientSession() as sesh:
        urls = await get_img_urls(sesh, 'https://en.wikipedia.org/wiki/Cold_War')
        print(len(urls))


if __name__ == '__main__':
    asyncio.run(main())
