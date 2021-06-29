import asyncio
import aiohttp
import time

async def get(url):
    # Async co routine
    try:
        async with aiohttp.ClientSession() as session:
            # All process shares the ClientSession
            async with session.get(url=url) as response:
                resp = await response.read() #Await: proceed to next task while waiting for response
                print("Succcesfully got url {} with response of length {}.".format(url, len(resp)))
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

async def main(urls):
    all_responses = await asyncio.gather(*[get(url) for url in urls])
    print("Finalized all. Return list of len {} outputs".format(len(all_responses)))

urls = ['https://www.google.com', 'https://www.youtube.com', 'https://www.facebook.com']
asyncio.run(main(urls))

