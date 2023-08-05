import logging


class RequestInfo(object):
    def __init__(self, url: str, proxy_url: str = None, user_agent: str = None, logger: logging.Logger=None):
        if not url:
            raise ValueError('URL is required!')
        self.url = url
        self.proxy_url = proxy_url
        self.headers = {}
        if user_agent:
            self.headers['User-Agent'] = user_agent
        self.string_to = url + ' ' + ('directly' if not proxy_url else 'via proxy {}'.format(repr(proxy_url)))
        self.logger = logger
        self.error = None
        self.result = None

    def started(self):
        if not self.logger:
            return
        self.logger.info('Connecting to {}'.format(self.string_to))

    def finished(self, error: str=None, result: str=None):
        self.error = error
        self.result = result
        if not self.logger:
            return
        if error:
            self.logger.error('Error connecting to {}: {}'.format(self.string_to, error))
            return
        self.logger.info('Success! Connected to {}.'.format(self.string_to))
