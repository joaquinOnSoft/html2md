import logging
import os
import re
import urllib

import requests


class URLUtils:

    @staticmethod
    def is_html(path: str) -> bool:
        """
        Check if a file path is a HTML file.
        :param path: File's full path
        :return: True if is a HTML file, False in other case
        """
        return os.path.isfile(path) and (path.endswith(".html") or path.endswith(".htm"))

    @staticmethod
    def is_friendly_url(path: str) -> bool:
        """
        Check if a file path is a friendly URL.
        It consider a file path as a friendly URL when the path is a file and has no extension
        :param path: File's full path
        :return: True if is a friendly URL, False in other case
        """
        friendly_url = True

        # If the file name contains URL parameters
        # 'os.path.isfile' and 'os.path.isdir' returns false
        if os.path.isfile(path) or (not os.path.isfile(path) and not os.path.isdir(path)):
            last_dot = path.rfind(".")
            last_separator = path.rfind(os.path.sep)

            if last_separator < last_dot:
                friendly_url = False

        return friendly_url

    @staticmethod
    def is_twitter_status_url(url: str) -> bool:
        """
        Check if a file URL is a Twitter status URL
        :param url: URL to be evaluated
        :return: True if is a Twitter status URL, False in other case
        SEE: https://stackoverflow.com/questions/4138483/twitter-status-url-regex
        """
        found = re.search(r'^https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)$', url)
        return found is not None and len(found.regs) == 4

    @staticmethod
    def is_youtube_video_url(url: str) -> bool:
        """
        Check if a file URL is a YouTube video URL
        :param url: These are the types of URLs supported
            http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
            http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/QdK8U-VIH_o
            http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
            http://www.youtube.com/embed/0zM3nApSvMg?rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg
            http://youtu.be/0zM3nApSvMg
        :return: True if is a YouTube video URL, False in other case
        SEE: https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
        """
        found = re.search(r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\??v?=?))([^#\&\?]*).*', url)
        return found is not None and len(found.regs) > 7 and len(found[7]) == 11

    @staticmethod
    def get_youtube_video_id(url: str) -> str:
        """
        Get the video identifier from a YouTube URL
        :param url: These are the types of URLs supported
            http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
            http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/QdK8U-VIH_o
            http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
            http://www.youtube.com/embed/0zM3nApSvMg?rel=0
            http://www.youtube.com/watch?v=0zM3nApSvMg
            http://youtu.be/0zM3nApSvMg
        :return: identifier from a YouTube URL
        SEE: https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
        """
        identifier = None

        found = re.search(r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\??v?=?))([^#\&\?]*).*', url)
        if found is not None and len(found[7]) == 11:
            identifier = found[7]

        return identifier

    @staticmethod
    def check_url_exists(url: str, timeout=-1) -> bool:
        """
        Check if a certain website exists
        :param url: URL to be checked
        :param timeout: Connection time out in seconds (admits decimals, e.g. 1 or 0.750).
        Default value: -1 (No timeout)
        :return: True if exist, False in other case
        SEE: https://stackoverflow.com/questions/16778435/python-check-if-website-exists
        """
        exist = False
        if url is not None and url != "":
            if url != "http://www.upm.es/FuturosEstudiantes/Ingresar/Acceso/EvAU":
                try:
                    if timeout == -1:
                        response = requests.get(url)
                    else:
                        response = requests.get(url, timeout=timeout)
                    if response.status_code == 200:
                        exist = True
                        logging.debug(f"URL {url} is valid and exists on the internet")
                except requests.ConnectionError as e:
                    logging.warning(f"URL {url} does not exist on Internet.")
                except requests.exceptions.ReadTimeout as e:
                    logging.warning(f"(Timeout) URL {url} does not exist on Internet.")

        return exist

    @staticmethod
    def get_html_from_url(url: str, timeout=-1) -> str:
        html = ""

        if url is not None and url != "":
            hdr = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) '
                              'Chrome/23.0.1271.64 Safari/537.11',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset': 'utf-8,ISO-8859-1;q=0.7,*;q=0.3',
                'Accept-Encoding': 'utf-8, iso-8859-1;q=0.5',
                'Accept-Language': 'en-US,en;q=0.8',
                'Connection': 'keep-alive'}
            req = urllib.request.Request(url, headers=hdr)
            try:
                # if timeout is -1 (No limit) set a one hour limit
                if timeout == -1:
                    timeout = 3600

                with urllib.request.urlopen(req, timeout=timeout) as f:
                    charset = "utf-8"
                    if f.headers.get_content_charset() is not None:
                        charset = f.headers.get_content_charset()
                    html += f.read().decode(charset, errors='ignore')
            except urllib.error.URLError as e:
                logging.warning(f"Error reading URL: {url} : {e.reason}")
            except UnicodeDecodeError as e:
                logging.warning(f"Error reading URL: {url} Unicode decode error: {e.reason}")

        return html
