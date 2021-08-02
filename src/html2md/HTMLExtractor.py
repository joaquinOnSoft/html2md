import re
from urllib.parse import unquote

from html2md.URLUtils import URLUtils


class HTMLExtractor:

    def __init__(self, url, timeout: int = -1):
        """
        :param url: URL to be checked
        :param timeout: Connection time out in seconds (admits decimals, e.g. 1 or 0.750).
        Default value: -1 (No timeout)
        """
        self.url = url
        self.html = None

        if url is not None and not URLUtils.is_twitter_status_url(url):
            self.html = URLUtils.get_html_from_url(url, timeout)

    def get_title(self):
        title = None
        if self.html:
            title_elements = re.findall(r"<(TITLE|title).*?>(.+?)<\/(TITLE|title)>", self.html)
            if title_elements is not None and len(title_elements) > 0 and len(title_elements[0]) == 3:
                title = title_elements[0][1]
            else:
                h1_elements = re.findall(r"<(h1|H1).*?>(.*)<\/(h1|H1)>", self.html)
                if h1_elements is not None and len(h1_elements) > 0 and len(h1_elements[0]) == 3:
                    title = h1_elements[0][1]

        if title is None and not URLUtils.is_twitter_status_url(self.url):
            index_last_separator = self.url.rfind("/")
            index_question_mark = self.url.rfind("?")
            if index_last_separator > 0:
                if index_question_mark > 0:
                    title = unquote(self.url[(index_last_separator + 1): index_question_mark])
                else:
                    title = unquote(self.url[(index_last_separator + 1):])

        return title
