import requests
from typing import Iterable

from ._request import RequestInfo

SESSION = requests.Session()


def _process_request(request: RequestInfo):
    """ Make a GET request to the URL, optionally using a proxy URL."""
    proxies = None
    if request.proxy_url:
        # same proxy for both http and https URLs
        proxies = {
            'http': request.proxy_url,
            'https': request.proxy_url,
        }
    request.started()
    try:
        response = SESSION.get(request.url, headers=request.headers, proxies=proxies)
    except Exception as e:
        request.finished(error=str(e))
    else:
        request.finished(result=response.text)


def process_requests(request_infos: Iterable[RequestInfo]):
    """ Fetch test_url for each of the proxy URLs, printing the request output if output is True. """
    for request in request_infos:
        _process_request(request)
