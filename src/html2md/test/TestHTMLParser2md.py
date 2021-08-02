from unittest import TestCase

from ..HTML2md import HTMLParser2md


class TestHTMLParser2md(TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.parser = HTMLParser2md()

    def test_li(self):
        self.parser.nested_list.append("ul")
        self.assertEqual("\n   * ", self.parser.li())
        self.parser.nested_list.append("ol")
        self.assertEqual("\n      1. ", self.parser.li())

    def test_img(self):
        attrs = [("src", "img/fiquipedia.png"), ("alt", "Fiquipedia logo")]
        self.assertEqual("![Fiquipedia logo](img/fiquipedia.png \"Fiquipedia logo\")\n", self.parser.img(attrs))

        # The image is inside a link
        self.parser.href = "htt://www.fiquipedia.es"
        self.assertEqual("", self.parser.img(attrs))

    def test_img_with_title(self):
        attrs = [("src", "img/fiquipedia.png"), ("alt", "Fiquipedia logo"), ("title", "Fiquipedia")]
        self.assertEqual("![Fiquipedia logo](img/fiquipedia.png \"Fiquipedia\")\n", self.parser.img(attrs))

    def test_md(self):
        md = "---\n\n|  | \n### Recursos\n |  | \n"
        self.parser.md = md

        md_cleaned = "---\n\n### Recursos\n\n"
        self.assertEqual(md_cleaned, self.parser.md)
