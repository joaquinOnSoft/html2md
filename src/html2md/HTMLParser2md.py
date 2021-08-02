import logging
import re
from html.parser import HTMLParser

from html2md.HTML2mdConverter import HTML2mdConverter


class HTMLParser2md(HTMLParser):
    # Hyperlink tag: <a>
    HTML_TAG_A = "a"
    # Line break tag: <br>
    HTML_TAG_BR = "br"
    # Header leve 1: <h1>
    HTML_TAG_H1 = "h1"
    # Header leve 2: <h2>
    HTML_TAG_H2 = "h2"
    # Header leve 3: <h3>
    HTML_TAG_H3 = "h3"
    # Header leve 4: <h4>
    HTML_TAG_H4 = "h4"
    # Header leve 5: <h5>
    HTML_TAG_H5 = "h5"
    # Header leve 6: <h6>
    HTML_TAG_H6 = "h6"
    # Header leve 7: <h7>
    HTML_TAG_H7 = "h7"
    # Header leve 8: <h8>
    HTML_TAG_H8 = "h8"
    # Image tag: <img>
    HTML_TAG_IMG = "img"
    # List item tag: <li>
    HTML_TAG_LI = "li"
    # Table data tag: <td>
    HTML_TAG_OL = "ol"
    # Paragraph tag: <p>
    HTML_TAG_P = "p"
    # Table data tag: <td>
    HTML_TAG_TD = "td"
    # Table header tag: <th>
    HTML_TAG_TH = "th"
    # Table row tag: <tr>
    HTML_TAG_TR = "tr"
    # Unordered list tag: <ul>
    HTML_TAG_UL = "ul"

    def __init__(self, url: bool = False, timeout: int = -1):
        """
        :param url: (boolean) Use the page title, header of level 1 or the last section of the
        URL as URL description (only when URL link a description are the same). NOTE: This option can be slow
        :param timeout: Timeout, in seconds, to use in link validation connections. Default value "-1" (unlimited)
        """
        super().__init__()

        self.url = url
        self.timeout = timeout

        self.reset()
        self._md = ""

        # Attribute to manage nested lists
        self.nested_list = []

        # flag to identify tags in inside other tags data section
        self.last_tag_full_parsed = False

        # Attribute to identify header rows in tables
        self.last_cell = None
        self.cell_in_row_counter = 0

        # Attribute to manage <a> tags
        self.href = None
        self.a_data = None
        self.a_data = None

        # Ignore mode (some tags like header, footer, comments section will be ignored)
        self.ignore_tags = False
        self.ignore_tags_counter = 0

        # List with all the links found in the page
        self.links = []

    @property
    def md(self):
        # Google Sites generates the page's content inside a table
        # We just remove this markdown tag
        return re.sub(r'^(\s+\|  \| \n)', "\n", self._md, flags=re.MULTILINE)

    @md.setter
    def md(self, markdown):
        self._md = markdown

    def handle_starttag(self, tag, attrs):
        self.last_tag_full_parsed = False
        html2md = ""

        if HTML2mdConverter.is_tag_ignored(tag, attrs):
            self.ignore_tags = True

        if self.ignore_tags:
            # <input> tags are not closed on  google site header
            if tag != "input":
                self.ignore_tags_counter += 1
            return

        if tag == self.HTML_TAG_A:
            self.href = HTML2mdConverter.get_attribute_by_name(attrs, "href")
            self.a_data = ""

            self.links.append(self.href)
        elif tag == self.HTML_TAG_BR:
            # Ignore <br> inside a table cell
            if self.last_cell is None:
                html2md = HTML2mdConverter.br(attrs)
        elif tag == self.HTML_TAG_H1:
            html2md = HTML2mdConverter.H1
        elif tag == self.HTML_TAG_H2:
            html2md = HTML2mdConverter.H2
        elif tag == self.HTML_TAG_H3:
            html2md = HTML2mdConverter.H3
        elif tag == self.HTML_TAG_H4:
            html2md = HTML2mdConverter.H4
        elif tag == self.HTML_TAG_H5:
            html2md = HTML2mdConverter.H5
        elif tag == self.HTML_TAG_H6:
            html2md = HTML2mdConverter.H6
        elif tag == self.HTML_TAG_H7:
            html2md = HTML2mdConverter.H7
        elif tag == self.HTML_TAG_H8:
            html2md = HTML2mdConverter.H8
        elif tag == self.HTML_TAG_IMG:
            html2md = self.img(attrs)
        elif tag == self.HTML_TAG_LI:
            html2md = self.li()
        elif tag == self.HTML_TAG_TR:
            html2md = "\n| "
            self.last_cell = None
            self.cell_in_row_counter = 0
        elif tag == self.HTML_TAG_TH:
            self.last_cell = self.HTML_TAG_TH
            self.cell_in_row_counter += 1
        elif tag == self.HTML_TAG_TD:
            self.last_cell = self.HTML_TAG_TD
            self.cell_in_row_counter += 1
        elif tag == self.HTML_TAG_UL or tag == self.HTML_TAG_OL:
            self.__push_nested_list(tag)

        self._md += html2md

    def handle_endtag(self, tag):
        self.last_tag_full_parsed = True

        if self.ignore_tags:
            self.ignore_tags_counter -= 1
            if self.ignore_tags_counter == 0:
                self.ignore_tags = False
            return

        if tag == self.HTML_TAG_A:
            # ignore <a> tags used as anchors (it doesn't include a href attribute)
            if self.href is not None and self.href != "":
                self._md += HTML2mdConverter.a(self.href, self.a_data, self.url, self.timeout)
            self.href = None
            self.a_data = None
        elif tag == self.HTML_TAG_H1 or tag == self.HTML_TAG_H2 or \
                tag == self.HTML_TAG_H3 or tag == self.HTML_TAG_H4 or \
                tag == self.HTML_TAG_H5 or tag == self.HTML_TAG_H6 or \
                tag == self.HTML_TAG_H7 or tag == self.HTML_TAG_H8:
            self._md += "\n"
        elif tag == self.HTML_TAG_OL or tag == self.HTML_TAG_UL:
            self.__pop_nested_list()
            self._md += "\n"
        elif tag == self.HTML_TAG_P:
            self._md += self.p()
        elif tag == self.HTML_TAG_TD or tag == self.HTML_TAG_TH:
            self._md += " | "
        elif tag == self.HTML_TAG_TR:
            self._md += self.tr()

    def handle_data(self, data):
        if self.ignore_tags:
            return

        if re.sub(r'\s+', "", data) != "":
            # Manage nested content in <a> tag
            if self.href is not None:
                self.a_data += data
                return

            data = re.sub(r'\s+', " ", data)

            # Manage other tags
            switcher = {
                "b": HTML2mdConverter.strong(data),
                "code": HTML2mdConverter.code(data),
                "i": HTML2mdConverter.i(data),
                # <kbd> defines some text as keyboard input in a document:
                "kbd": HTML2mdConverter.var(data),
                "li": data.strip(),
                "pre": HTML2mdConverter.code(data),
                # <samp> defines some text as sample output from a computer program in a document
                "samp": HTML2mdConverter.var(data),
                "script": HTML2mdConverter.ignore_tag(data),
                "strong": HTML2mdConverter.strong(data),
                "style": HTML2mdConverter.ignore_tag(data),
                # "title": HTML2mdConverter.title(data),
                "title": HTML2mdConverter.ignore_tag(data),
                # The <var> tag is used to defines a variable in programming or
                # in a mathematical expression. The content inside is typically displayed in italic.
                "var": HTML2mdConverter.var(data)
            }

            # Manage nested tag properly
            if self.last_tag_full_parsed:
                html2md = HTML2mdConverter.default_tag(data)
            else:
                html2md = switcher.get(self.lasttag, HTML2mdConverter.default_tag(data))

            self._md += html2md

    def handle_comment(self, data):
        return HTML2mdConverter.comment(data)

    def error(self, message):
        logging.debug(message)

    def __push_nested_list(self, tag: str):
        self.nested_list.append(tag)

    def __pop_nested_list(self) -> str:
        return self.nested_list.pop()

    def li(self) -> str:
        size = len(self.nested_list)
        if size > 0:
            filler = "\n"
            for step in range(size):
                filler += "   "

            last_list_tag = self.nested_list[-1]
            if last_list_tag == "ul":
                return filler + "* "
            elif last_list_tag == "ol":
                return filler + "1. "
        else:
            return ""

    def tr(self) -> str:
        table_row_md = ""

        if self.last_cell == self.HTML_TAG_TH:
            for x in range(self.cell_in_row_counter):
                table_row_md += "| --- "
            table_row_md = "\n" + table_row_md + "| "

        return table_row_md

    def img(self, attrs):
        img = HTML2mdConverter.img(attrs)

        if self.href:
            if self.a_data is None:
                self.a_data = ""
            self.a_data += img
            img = ""

        return img

    def p(self):
        md = ""
        # Don't add a line break inside a table cell
        if self.last_cell is None:
            md = "\n"
        return md
