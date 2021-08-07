import copy
import logging
import os
import shutil

from html2md.HTMLParser2md import HTMLParser2md
from html2md.URLUtils import URLUtils


class HTML2md:

    @staticmethod
    def process(source: str, destination: str, url: bool, timeout: int, multiline: bool = False):
        """
        Convert and HTML file or folder (with all their nested files) in a Markdown file.
        :param source:  source file or folder
        :param destination: destination file or folder
        :param url: (boolean) Use the page title, header of level 1 or the last section of the
        URL as URL description (only when URL link a description are the same). NOTE: This option can be slow
        :param timeout: Timeout, in seconds, to use in link validation connections. Default value "-1" (unlimited)
        :param multiline: (boolean) Support for multiline content in table cells. (WARNING: Google Sites may
        use internal tables in HTML which may not seem tables for the user. Use under your own risk!)
        """
        if os.path.isfile(source):
            HTML2md.__process_file(source, destination, url, timeout, multiline)
        else:
            HTML2md.__process_folder(source, destination, url, timeout, multiline)

    @staticmethod
    def __process_folder(source: str, destination: str, url: bool, timeout: int, multiline: bool = False):

        for dir_path, dirs, files in os.walk(source):

            for d in dirs:
                d_in_name = os.path.join(source, os.path.join(dir_path, d))
                d_out_name = d_in_name.replace(source, destination)
                if not os.path.exists(d_out_name):
                    logging.debug("Creating folder: " + d_out_name)
                    os.mkdir(d_out_name)

            for filename in files:
                f_in_name = os.path.join(dir_path, filename)
                f_out_name = f_in_name.replace(source, destination)

                if URLUtils.is_friendly_url(f_in_name):
                    f_out_name = f_out_name + ".md"
                    logging.debug("HTML2MD: " + f_in_name)

                    HTML2md.__process_file(f_in_name, f_out_name, url, timeout, multiline)
                elif URLUtils.is_html(f_in_name):
                    f_out_name = f_out_name.replace(".html", ".md").replace(".htm", ".md")
                    logging.debug("HTML2MD: " + f_in_name)

                    HTML2md.__process_file(f_in_name, f_out_name, url, timeout, multiline)
                else:
                    logging.debug("Copying: " + f_in_name)
                    shutil.copy2(f_in_name, f_out_name)

    @staticmethod
    def __process_file(source: str, destination: str, url: bool, timeout: int, multiline: bool = False):
        """
        Convert and HTML file in a Markdown file.
        :param source:  source file or folder
        :param destination: destination file or folder
        :param url: (boolean) Use the page title, header of level 1 or the last section of the
        URL as URL description (only when URL link a description are the same). NOTE: This option can be slow
        :param timeout: Timeout, in seconds, to use in link validation connections. Default value "-1" (unlimited)
        """
        f = open(source, "r")
        html_txt = f.read()
        f.close()

        # Parse html file
        parser = HTMLParser2md(url, timeout, multiline)
        parser.feed(html_txt)
        md = parser.md

        md = HTML2md.__remove_useless_md(md)

        if destination is None:
            destination = source.replace('.html', '.md').replace('.htm', '.md')
        f = open(destination, "w")
        f.write(md)
        f.close()

    @staticmethod
    def __remove_useless_md(md: str) -> str:
        if md is not None:
            md = md.replace("\n|  | \n", "")

        return md
