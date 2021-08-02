import unittest

from gsites2md.HTMLExtractor import HTMLExtractor


class TestHTMLExtractor(unittest.TestCase):
    def test_get_title(self):
        extractor = HTMLExtractor("https://www.educaciontrespuntocero.com/experiencias/"
                                  "frikiexamenes-estres-estudiantes/")
        self.assertEqual("Frikiexámenes para implicar y reducir el estrés de los estudiantes", extractor.get_title())

        extractor = HTMLExtractor("https://rseq.org/mat-didacticos/"
                                  "resumen-de-las-normas-iupac-2005-de-nomenclatura-de-quimica-inorganica-"
                                  "para-su-uso-en-ensenanza-secundaria-y-recomendaciones-didacticas/")
        self.assertEqual("Resumen de las normas IUPAC 2005 de nomenclatura de Química Inorgánica para su uso en "
                         "enseñanza secundaria y recomendaciones didácticas &ndash; RSEQ", extractor.get_title())

    def test_get_title_with_attributes(self):
        extractor = HTMLExtractor("https://www.geogebra.org/m/wgppdvnm")
        self.assertEqual("FQ3ESO T05 Representa gráfica e-t – GeoGebra", extractor.get_title())

    def test_get_title_with_uppercase(self):
        extractor = HTMLExtractor("http://hyperphysics.phy-astr.gsu.edu/hbase/Waves/string.html")
        self.assertEqual("Standing Waves on a String", extractor.get_title())



    def test_get_title_from_none_html(self):
        extractor = HTMLExtractor("https://rseq.org/wp-content/uploads/2018/09/5-OtrosMateriales.pdf#page=2", 5)
        self.assertEqual("5-OtrosMateriales.pdf#page=2", extractor.get_title())

    def test_get_title_from_none_html_with_params(self):
        extractor = HTMLExtractor("https://www.fiquipedia.es/home/recursos/ejercicios/"
                                  "ejercicios-elaboracion-propia-fisica-2-bachillerato/"
                                  "ProblemaGravitacion2.pdf?attredirects=0")
        self.assertEqual("ProblemaGravitacion2.pdf", extractor.get_title())


if __name__ == '__main__':
    unittest.main()
