import asyncio

import aiohttp

from flags import main, save_flag, show


BASE_URL = 'http://127.0.0.1:8001/flags'


async def get_flag(session, cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    async with session.get(url) as resp:
        image = await resp.read()
    return image


async def download_one(session, cc):
    image = await get_flag(session, cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        to_do = [download_one(session, cc) for cc in sorted(cc_list)]
        wait_coro = asyncio.wait(to_do)
        res, _ = loop.run_until_complete(wait_coro)

    return len(res)


if __name__ == '__main__':
    main(download_many)
