import asyncio

import aiohttp

from flags import main, save_flag, show

#与flags_asyncio.py中不同的使用session.get()的方式
BASE_URL = 'http://127.0.0.1:8001/flags'


async def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            image = await resp.read()
    return image


async def download_one(cc):
    image = await get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ = loop.run_until_complete(wait_coro)

    return len(res)


if __name__ == '__main__':
    main(download_many)
