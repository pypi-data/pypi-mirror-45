
from logging import getLogger
from aiohttp import ClientSession


class PostmarkClient(object):
    """

    Example:

    curl "https://api.postmarkapp.com/email" \
        -X POST \
        -H "Accept: application/json" \
        -H "Content-Type: application/json" \
        -H "X-Postmark-Server-Token: server token" \
        -d "{From: 'sender@example.com', To: 'receiver@example.com', Subject: 'Postmark test', HtmlBody: '<html><body><strong>Hello</strong> dear Postmark user.</body></html>'}"

    """

    def __init__(self, server_token):
        self.__log = getLogger('aiopm')
        self._url = 'https://api.postmarkapp.com/email'
        self._server_token = server_token

    async def send(self, From, To, Subject, HtmlBody):
        """ Delivery email message

        Args:

        """
        payload = {
            'From': From,
            'To': To,
            'Subject': Subject,
            'HtmlBody': HtmlBody,
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Postmark-Server-Token': self._server_token,
        }
        #
        async with ClientSession() as session:
            async with session.post(self._url, json=payload, headers=headers) as resp:
                self.__log.debug("status = {status!r}".format(status=resp.status))
                if resp.status != 200:
                    content = await resp.text()
                    raise RuntimeError('Postmark response code {status} and content {content}'.format(status=resp.status, content=content))
                values = await resp.json()
                return values
