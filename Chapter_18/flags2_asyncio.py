import asyncio
import collections
import sys
from os import path

import aiohttp
from aiohttp import web
import tqdm


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from Chapter_17.flags2_common import main, save_flag, HTTPStatus, Result


DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000


class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code


async def get_flag(session, base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = await session.get(url)
    if resp.status == 200:
        image = await resp.read()
        return image
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(
            code = resp.status,
            message = resp.reason,
            headers = resp.headers,
        )


async def download_one(session, cc, base_url, semaphore, verbose):
    try:
        with (await semaphore):
            image = await get_flag(session, base_url, cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)


async def downloader_coro(session, cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)
    to_do = [download_one(session, cc, base_url, semaphore, verbose)
            for cc in sorted(cc_list)]

    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
    for future in to_do_iter:
        try:
            res = await future
        except FetchError as exc:
            country_code = exc.country_code
            try:
                error_msg = exc.__cause__.args[0]
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status

        counter[status] += 1

    return counter


def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        coro = downloader_coro(session, cc_list, base_url, verbose, concur_req)
        counts = loop.run_until_complete(coro)

    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
