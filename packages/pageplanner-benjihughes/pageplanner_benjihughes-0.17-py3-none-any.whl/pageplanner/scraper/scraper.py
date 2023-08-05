from requests_html import HTMLSession
from urllib.parse import urlparse
import urllib3
import logging
from pageplanner.scraper.exceptions import ScrapeError
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.getLogger(urllib3.__package__).setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

class Scraper:

    def __init__(self):
        self.session = self.get_requests_session()

    def scrape(self, url):
        """
        Scrapes the given URL and returns the raw content response.

        :param url:
        :return requests_html.HTML:
        """

        # Update Host header in session.
        host = urlparse(url).hostname
        if host:
            self.session.headers.update({
                'Host': host
            })

        response = self.session.get(url, verify=False, timeout=10, allow_redirects=True)

        # Requests follows redirects, so if we don't end up on a 200 eventually, we probably didn't
        # get the page we were hoping for.
        if response.status_code != 200:
            raise ScrapeError('Server responded with code: %s' % response.status_code)

        # If there's no content, we definitely want to know about it.
        if len(response.content.strip()) == 0:
            raise ScrapeError('Server responded with an empty response body')

        # Similarly, if the response object has no HTML attribute, something has gone wrong.
        if not hasattr(response, 'html'):
            raise ScrapeError('No HTML attribute present on response object')

        # Render the HTML in a Chromium browser to get content post-javascript.
        # response.html.render()

        logger.info('Scraped %s succesfully.' % url)

        # Return the HTML object ready for parsing.
        return response.html

    @staticmethod
    def get_requests_session():
        session = HTMLSession()
        session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Pragma': 'no-cache',
            'TE': 'Trailers',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
        })
        return session
