import os
from unittest import TestCase

from ..HTML2md import HTML2md


class TestHTML2md(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.base_path += "/../../../resources/"

    @staticmethod
    def read_file(file_name: str) -> str:
        f = open(file_name, "r")
        txt = f.read()
        f.close()
        return txt

    def test_header(self):
        self.__process("test-header.html", "test-header.md")

    def test_list(self):
        self.__process("test-list.html", "test-list.md")

    def test_script(self):
        self.__process("test-script.html", "test-script.md")

    def test_table(self):
        self.__process("test-table.html", "test-table.md")

    def test_table_from_gsites(self):
        """
        Test the conversion of a HTML that includes `rowspand` and `cellspand` attributes.
        Those attributes are not supported by Markdown, so the conversion is not perfect :-(
        :return:
        """
        self.__process("test-table-from-gsites.html", "test-table-from-gsites.md")

    def test_table_ignored_from_gsites(self):
        self.__process("test-table-ignored-from-gsites.html", "test-table-ignored-from-gsites.md")

    def test_table_of_hell(self):
        self.__process("test-table-of-hell.html", "test-table-of-hell.md")

    def test_table_recursos_opos(self):
        self.__process("test-table-recursos-opos.html", "test-table-recursos-opos.md")

    # def test_pau_fisica(self):
    #    self.__process("fiquipedia.es/pruebasaccesouniversidad/paufisica.html", "test-header.md")

    def test_recursos_tecnologia(self):
        self.__process("fiquipedia.es/recursos/recursos-tecnologia.html",
                       "fiquipedia.es/recursos/recursos-tecnologia.md")

    def test_ignore_toc(self):
        self.__process("fiquipedia.es/recursos/recursospau/recursos-pau-genericos.html",
                       "fiquipedia.es/recursos/recursospau/recursos-pau-genericos.md")

    def test_ignore_gsites_header(self):
        self.__process("test-ignore-gsites-header.html", "test-ignore-gsites-header.md")

    def test_ignore_gsites_footer(self):
        self.__process("test-ignore-gsites-footer.html", "test-ignore-gsites-footer.md")

    def __process(self, input_file_name: str, output_file_name: str):
        input_file_name = self.base_path + input_file_name
        output_file_name = self.base_path + output_file_name

        generated_output_file_name = input_file_name + ".md"

        # Generate friendly URL descriptions
        HTML2md.process(input_file_name, generated_output_file_name, True, 5)

        expected_output = TestHTML2md.read_file(output_file_name)
        generated_output = TestHTML2md.read_file(generated_output_file_name)

        self.assertEqual(expected_output, generated_output)

        # Remove generated file during the test
        os.remove(generated_output_file_name)
