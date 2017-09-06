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


async def http_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            if res.status == 200:
                ctype = res.headers.get('Content-type', '').lower()
                if ('json' in ctype) or url.endswith('json'):
                    data = await res.json()
                else:
                    data = await res.read()
                return data

            elif res.status == 404:
                raise web.HTTPNotFound()
            else:
                raise aiohttp.http_exceptions.HttpProcessingError(
                    code=res.status,
                    message=res.reason,
                    headers=res.headers
                )


async def get_country(base_url, cc):
    url = '{}/{cc}/metadata.json'.format(base_url, cc=cc.lower())
    metadata = await http_get(url)
    return metadata['country']


async def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    return (await http_get(url))


async def download_one(cc, base_url, semaphore, verbose):
    try:
        with (await semaphore):
            image = await get_flag(base_url, cc)
        with (await semaphore):
            country = await get_country(base_url, cc)
    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:
        country = country.replace(' ', '_')
        filename = '{}-{}.gif'.format(country, cc)
        loop = asyncio.get_event_loop()
        #异步中也可以执行其它线程，从而避免某些阻塞
        loop.run_in_executor(None, save_flag, image, filename)
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)


async def downloader_coro(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    semaphore = asyncio.Semaphore(concur_req)
    to_do = [download_one(cc, base_url, semaphore, verbose)
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
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
    loop.close()

    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
