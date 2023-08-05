import asyncio
import logging
from typing import List, Iterable
import aiohttp

from ._request import RequestInfo


LOGGER = logging.getLogger('proxytest.async')


async def process_requests(request_infos: Iterable[RequestInfo]):
    """ Fetch test_url for each of the proxy URLs, printing the request output if output is True. """
    loop = asyncio.get_event_loop()
    fail_count = loop.run_until_complete(process_requests_async(request_infos))
    return fail_count


async def process_requests_async(request_infos: Iterable[RequestInfo]):
    async with aiohttp.ClientSession() as session:
        # TODO: all at once!
        for request in request_infos:
            await _process_request(session=session, request=request)


async def _process_request(session: aiohttp.ClientSession, request: RequestInfo):
    async with session.get(request.url, proxy=request.proxy_url, headers=request.headers) as response:
        try:
            response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            LOGGER.error('ERROR: could not connect to {}: {}'.format(request.string_to, e))
            return None
        else:
            text = await response.text()
            LOGGER.info('Success! Got {:,} characters with status {}. Preview: {}'.format(len(text), response.status, repr(text[:100] + '...')))
            return text


