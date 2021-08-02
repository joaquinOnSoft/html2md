import logging
import re
from urllib.parse import unquote

from gsites2md.HTMLExtractor import HTMLExtractor
from gsites2md.URLUtils import URLUtils


class HTML2mdConverter:
    H1 = "\n\n# "
    H2 = "\n\n## "
    H3 = "\n\n### "
    H4 = "\n\n#### "
    H5 = "\n\n##### "
    H6 = "\n\n###### "
    H7 = "\n\n####### "
    H8 = "\n\n######## "

    INDEX_TAG = 0
    INDEX_ATTRIBUTE_NAME = 1
    INDEX_ATTRIBUTE_VALUE = 2

    @staticmethod
    def a(href: str, data: str, friendly_url_desc: bool = False, timeout: float = -1) -> str:
        if data is not None:
            if data == href and friendly_url_desc:
                # Replace link description with the page title instead
                # of using the URL as description
                logging.debug(f"Replace link description with the page title {href}")
                extractor = HTMLExtractor(href, timeout)
                title = extractor.get_title()
                if title is not None:
                    data = title
            else:
                data = re.sub(r'\s+', " ", data)

                # Replace Google Sites backup site URL for main site URLs
                data = HTML2mdConverter.__replace_fiquipedia_backup_site(data)
                # Replace MEC urls for the new one
                data = HTML2mdConverter.__replace_mec_url_by_educacionyfp(data)

                # Url decode UTF-8 in Python
                # https://stackoverflow.com/questions/16566069/url-decode-utf-8-in-python
                data = unquote(data)
        else:
            data = ""

        if URLUtils.is_youtube_video_url(href):
            return HTML2mdConverter.a_youtube(URLUtils.get_youtube_video_id(href), data)

        if href:
            # Replace absolute URL with local paths
            href = HTML2mdConverter.__replace_fiquipedia_url_with_local_path(href)

            # Can all the '?attredirects=0' be automatically removed from URLs?
            href = HTML2mdConverter.__remove_attredirects_param_from_url(href)

            # Replace MEC urls for the new one
            href = HTML2mdConverter.__replace_mec_url_by_educacionyfp(href)

            # Remove ".html" extension from fiquipedia URL
            href = HTML2mdConverter.__remove_html_extension_from_fiquipedia_url(href)

        if href == "":
            href = "/"

        return f' [{data}]({href}) '

    @staticmethod
    def blockquote(data: str) -> str:
        quote = ""
        for line in data.splitlines():
            quote += "> " + line + "\n"
        return quote

    @staticmethod
    def br(data: str) -> str:
        return "\n"

    @staticmethod
    def code(data: str) -> str:
        """
        Manage <code> and <pre> tags
        :param data: text preformatted, usually code.
        :return: Markdown for Syntax highlighting
        """
        return "\n```\n" + data + "\n```\n"

    @staticmethod
    def h1(data: str) -> str:
        return "\n\n# " + data + "\n"

    @staticmethod
    def h2(data: str) -> str:
        return "\n\n## " + data + "\n"

    @staticmethod
    def h3(data: str) -> str:
        return "\n\n### " + data + "\n"

    @staticmethod
    def h4(data: str) -> str:
        return "\n\n#### " + data + "\n"

    @staticmethod
    def h5(data: str) -> str:
        return "\n\n##### " + data + "\n"

    @staticmethod
    def h6(data: str) -> str:
        return "\n\n###### " + data + "\n"

    @staticmethod
    def h7(data: str) -> str:
        return "\n\n####### " + data + "\n"

    @staticmethod
    def h8(data: str) -> str:
        return "\n\n######## " + data + "\n"

    @staticmethod
    def i(data: str) -> str:
        return "*" + data + "*"

    @staticmethod
    def img(attrs) -> str:
        """
        Generate the 'img' tag in markdown. The output will looks like this:
            ![Alt](/path/to/img.jpg “image title”)
        :param attrs: Attributes list of the img tag
        :return: img tag in markdown
        SEE: https://dev.to/stephencweiss/markdown-image-titles-and-alt-text-5fi1
        """
        link = HTML2mdConverter.get_attribute_by_name(attrs, "src")
        alt = HTML2mdConverter.get_attribute_by_name(attrs, "alt")
        title = HTML2mdConverter.get_attribute_by_name(attrs, "title")
        if title is None or title == "":
            title = alt

        return f'![{alt}]({link} "{title}")\n'

    @staticmethod
    def strong(data: str) -> str:
        return "**" + data + "**"

    @staticmethod
    def title(data: str) -> str:
        meta = "---\n"
        meta += f'title: {data.replace(":", " -")}\n'
        meta += "---\n"
        return meta

    @staticmethod
    def var(data: str) -> str:
        """
        Manage <var>, <samp> and <kbd> tags.
        :param data: text used to defines a variable in programming or in a mathematical expression.
        :return: Markdown for Inline code
        """
        return "`" + data + "`"

    @staticmethod
    def comment(data: str) -> str:
        """
        Manage HTML comments
        SEE: https://stackoverflow.com/questions/4823468/comments-in-markdown
        :param data: Text inside the comment tag
        :return: Markdown for HTML comment
        """
        comment = data.replace("\n", " ")
        return f'[//]: # ({comment})'

    @staticmethod
    def default_tag(data) -> str:
        return data

    @staticmethod
    def ignore_tag(data) -> str:
        return ""

    @staticmethod
    def get_attribute_by_name(attrs, attr_name):
        for name, value in attrs:
            if name == attr_name:
                return value
        return ""

    @staticmethod
    def is_tag_ignored(tag: str, attrs) -> bool:
        """
        Check if the and specific tag + its attributes must be ignored or not.
        These are the tags included by Google Sites that will be mark to be ignored:
           - Google sites header: `<table id="sites-chrome-header">
           - Google sites comments area: `<div id="sites-canvas-bottom-panel">`
           - Google sites footer: `<div id="sites-chrome-adminfooter-container">`
        :param tag: Tag name
        :param attrs: Tag's attributes list (key - value pairs)
        :return: True if the tag must be ignored, False in other case
        """
        ignore = False
        # Array that contains tag that must be ignored: Tag name, Attribute name, Attribute value
        ignore_list = [
            # Google sites header
            ["table", "id", "sites-chrome-header"],
            # Google sites breadcrumbs
            ["div", "id", "title-crumbs"],
            # Google sites comments area
            ["div", "id", "sites-canvas-bottom-panel"],
            # Google sites footer
            ["div", "id", "sites-chrome-footer"],
            # Google sites admin footer
            ["div", "id", "sites-chrome-adminfooter-container"],
            # Table Of Contents (TOC)
            ["div", "class", "goog-toc sites-embed-toc-maxdepth-6"]
        ]

        for i_tag in ignore_list:
            if i_tag[HTML2mdConverter.INDEX_TAG] == tag:
                attr_value = HTML2mdConverter.get_attribute_by_name(attrs, i_tag[HTML2mdConverter.INDEX_ATTRIBUTE_NAME])
                if i_tag[HTML2mdConverter.INDEX_ATTRIBUTE_VALUE] == attr_value:
                    ignore = True

        return ignore

    @staticmethod
    def __replace_fiquipedia_url_with_local_path(url: str) -> str:
        """
        Replace absolute fiquipedia URL with local paths
        :param url: url to be evaluated
        :return: local path if is a fiquipedia URL, the original URL in other case
        """
        path = url

        if url is not None:
            path = url.replace("http://fiquipedia.es", "") \
                .replace("http://www.fiquipedia.es", "") \
                .replace("https://fiquipedia.es", "") \
                .replace("https://www.fiquipedia.es", "") \
                .replace("http://sites.google.com/site/fiquipediabackup05mar2018", "") \
                .replace("https://sites.google.com/site/fiquipediabackup05mar2018", "") \
                .replace("http://a0286e09-a-62cb3a1a-s-sites.googlegroups.com/site/fiquipediabackup05mar2018", "")

        return path

    @staticmethod
    def __remove_attredirects_param_from_url(url: str) -> str:
        """
        Remove all the '?attredirects=0' parameters from Google Drive URLs
        :param url: url to be evaluated
        :return: Google Drive without the '?attredirects=0' parameter, the original URL in other case

        """
        new_url = url

        if url is not None:
            # Can all the '?attredirects=0' be automatically removed from URLs?
            index_att_redirects = url.find("?attredirects=0")
            if index_att_redirects != -1:
                new_url = url[0:index_att_redirects]

        return new_url

    @staticmethod
    def __remove_html_extension_from_fiquipedia_url(url: str) -> str:
        new_url = url

        if url is not None:
            # Remove ".html" extension from fiquipedia URL
            if (url.startswith("http://www.fiquipedia.es") or
                url.startswith("https://www.fiquipedia.es") or
                url.startswith("..") or url.startswith("/")) and \
                    (url.endswith(".html") or url.endswith(".html")):
                new_url = url.replace(".html", "").replace(".htm", "")

        return new_url

    @staticmethod
    def __replace_mec_url_by_educacionyfp(url: str) -> str:
        """
        Replace MEC urls for the new one
        :param url:
        :return:
        """
        new_url = url

        if url is not None:
            if url.startswith("http://www.mecd.gob.es"):
                new_url = url.replace("http://www.mecd.gob.es", "http://www.educacionyfp.gob.es")

        return new_url

    @staticmethod
    def __replace_fiquipedia_backup_site(url: str) -> str:
        """
        Replace Google Sites backup site URL for main site URLs
        :param url:
        :return:
        """
        new_url = url

        if url is not None:
            new_url = url.replace("http://sites.google.com/site/fiquipediabackup05mar2018", "https://www.fiquipedia.es") \
                .replace("https://sites.google.com/site/fiquipediabackup05mar2018", "https://www.fiquipedia.es")

        return new_url

    @staticmethod
    def a_youtube(video_id: str, title: str) -> str:
        """
        Generate a link to a YouTube video in markdown using a preview image:
            [![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/YOUTUBE_VIDEO_ID_HERE/0.jpg)]
            (https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID_HERE)
        :param video_id: Video identifier
        :param title: Video's title
        :return:
        SEE: https://stackoverflow.com/questions/2068344/how-do-i-get-a-youtube-video-thumbnail-from-the-youtube-api?rq=1
        SEE: https://stackoverflow.com/questions/11804820/how-can-i-embed-a-youtube-video-on-github-wiki-pages
        """
        return f" [![{title}](https://img.youtube.com/vi/{video_id}/0.jpg)](https://www.youtube.com/watch?v={video_id}) "
