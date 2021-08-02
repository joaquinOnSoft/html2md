from unittest import TestCase

from ..HTML2mdConverter import HTML2mdConverter


class TestHTML2mdConverter(TestCase):

    def test_a(self):
        self.assertEqual(" [Fiquipedia](/) ", HTML2mdConverter.a("https://fiquipedia.es", "Fiquipedia"))
        self.assertEqual(" [Fiquipedia](/) ", HTML2mdConverter.a("https://www.fiquipedia.es", "Fiquipedia"))
        self.assertEqual(" [Fiquipedia](/) ", HTML2mdConverter.a("http://fiquipedia.es", "Fiquipedia"))
        self.assertEqual(" [Fiquipedia](/) ", HTML2mdConverter.a("http://www.fiquipedia.es", "Fiquipedia"))
        self.assertEqual(" [Fiquipedia is cool](/) ",
                         HTML2mdConverter.a("http://fiquipedia.es", "Fiquipedia \n\n\t is cool"))
        self.assertEqual(" [Recursos](/recursos) ", HTML2mdConverter.a("/recursos", "Recursos"))
        self.assertEqual(" [Github](http://www.github.com) ", HTML2mdConverter.a("http://www.github.com", "Github"))

    def test_a_remove_att_redirects(self):
        self.assertEqual(" [Andalucía FQ enunciados](/home/recursos/recursos-para-oposiciones"
                         "/2021-06-19-Andaluc%C3%ADa-FQ-enunciados.pdf) ",
                         HTML2mdConverter.a("http://www.fiquipedia.es/home/recursos/recursos-para-oposiciones/2021-06"
                                            "-19-Andaluc%C3%ADa-FQ-enunciados.pdf?attredirects=0", "Andalucía FQ enunciados"))

    def test_a_remove_html_extension(self):
        self.assertEqual(" [Evaluaciones](../evaluaciones-finales-bachillerato) ",
                         HTML2mdConverter.a("../evaluaciones-finales-bachillerato.html", "Evaluaciones"))
        self.assertEqual(" [PAU Fisica](/recursospau/pau-fisica) ",
                         HTML2mdConverter.a("https://www.fiquipedia.es/recursospau/pau-fisica.html", "PAU Fisica"))

    def test_a_remove_html_extension_2(self):
        self.assertEqual(
            " [Dictamen 142016](http://www.educacionyfp.gob.es/dctm/cee/el-consejo/dictamenes/2016/dictamen142016.pdf) ",
            HTML2mdConverter.a("http://www.mecd.gob.es/dctm/cee/el-consejo/dictamenes/2016/dictamen142016.pdf",
                               "Dictamen 142016"))

    def test_a_site_google_groups_com(self):
        self.assertEqual(
            " [Problemas Fisica Dinamica Presion](/home/recursos/fisica/recursos-dinamica/ProblemasFisica-Dinamica"
            "-Presion.pdf) ",
            HTML2mdConverter.a("http://a0286e09-a-62cb3a1a-s-sites.googlegroups.com/site/fiquipediabackup05mar2018"
                               "/home/recursos/fisica/recursos-dinamica/ProblemasFisica-Dinamica-Presion.pdf",
                               "Problemas Fisica Dinamica Presion"))

    def test_a_with_fiquipedia_backup_link(self):
        url = "https://sites.google.com/site/fiquipediabackup05mar2018/home/recursos/ejercicios/ejercicios" \
              "-elaboracion-propia-fisica-2-bachillerato/ProblemaGravitacion2.pdf?attredirects=0"
        expected_url_link = "/home/recursos/ejercicios/ejercicios" \
                            "-elaboracion-propia-fisica-2-bachillerato/ProblemaGravitacion2.pdf"
        expected_url_text = "ProblemaGravitacion2.pdf"
        self.assertEqual(f' [{expected_url_text}]({expected_url_link}) ', HTML2mdConverter.a(url, url, True, 5))

    def test_a_with_white_spaces(self):
        # <a href="https://www.serina.es/empresas/cede_muestra/106/TEMA%20MUESTRA.pdf">
        #   https://www.serina.es/empresas/cede_muestra/106/TEMA%20MUESTRA.pdf
        # </a>
        url = "https://www.serina.es/empresas/cede_muestra/106/TEMA%20MUESTRA.pdf"
        expected_url_text = "TEMA MUESTRA.pdf"
        expected_url_link = "https://www.serina.es/empresas/cede_muestra/106/TEMA%20MUESTRA.pdf"
        self.assertEqual(f' [{expected_url_text}]({expected_url_link}) ', HTML2mdConverter.a(url, url, True, 2))

    def test__a_youtube(self):
        self.assertEqual(" [![Joaquín Sabina La del Pirata Cojo](https://img.youtube.com/vi/MJF0dbZCVgQ/0.jpg)]"
                         "(https://www.youtube.com/watch?v=MJF0dbZCVgQ) ",
                         HTML2mdConverter.a_youtube("MJF0dbZCVgQ", "Joaquín Sabina La del Pirata Cojo"))

    def test_blockquote(self):
        quote = "This is the AK-47 assault rifle, \nthe preferred weapon of your enemy;"
        md_quote = "> This is the AK-47 assault rifle, \n> the preferred weapon of your enemy;\n"
        self.assertEqual(md_quote, HTML2mdConverter.blockquote(quote))

    def test_code(self):
        self.assertEqual("\n```\nalert( 'Hello, world!' );\n```\n", HTML2mdConverter.code("alert( 'Hello, world!' );"))

    def test_h1(self):
        self.assertEqual("\n\n# Hello\n", HTML2mdConverter.h1("Hello"))

    def test_h2(self):
        self.assertEqual("\n\n## Hello\n", HTML2mdConverter.h2("Hello"))

    def test_h3(self):
        self.assertEqual("\n\n### Hello\n", HTML2mdConverter.h3("Hello"))

    def test_h4(self):
        self.assertEqual("\n\n#### Hello\n", HTML2mdConverter.h4("Hello"))

    def test_h5(self):
        self.assertEqual("\n\n##### Hello\n", HTML2mdConverter.h5("Hello"))

    def test_h6(self):
        self.assertEqual("\n\n###### Hello\n", HTML2mdConverter.h6("Hello"))

    def test_h7(self):
        self.assertEqual("\n\n####### Hello\n", HTML2mdConverter.h7("Hello"))

    def test_h8(self):
        self.assertEqual("\n\n######## Hello\n", HTML2mdConverter.h8("Hello"))

    def test_i(self):
        self.assertEqual("*Hello*", HTML2mdConverter.i("Hello"))

    def test_img(self):
        attrs = [("src", "img/picture1.png"), ("alt", "My first picture")]
        self.assertEqual("![My first picture](img/picture1.png \"My first picture\")\n", HTML2mdConverter.img(attrs))

    def test_strong(self):
        self.assertEqual("**Hello**", HTML2mdConverter.strong("Hello"))

    def test_var(self):
        self.assertEqual("`File not found.`", HTML2mdConverter.var("File not found."))

    def test_get_attribute_by_name(self):
        attrs = [('src', 'my-image.png'), ('href', 'index.html')]
        self.assertEqual("index.html", HTML2mdConverter.get_attribute_by_name(attrs, "href"))
        self.assertEqual("", HTML2mdConverter.get_attribute_by_name(attrs, "href2"))

    def test_is_tag_ignored(self):
        attrs = [('style', 'font-color: red'), ('id', 'sites-chrome-header')]
        self.assertTrue(HTML2mdConverter.is_tag_ignored("table", attrs))

        attrs = [('style', 'font-color: red'), ('id', 'sites-canvas-bottom-panel')]
        self.assertTrue(HTML2mdConverter.is_tag_ignored("div", attrs))

        attrs = [('style', 'font-color: red'), ('id', 'sites-chrome-adminfooter-container')]
        self.assertTrue(HTML2mdConverter.is_tag_ignored("div", attrs))

        attrs = [('style', 'font-color: red'), ('id', 'my-table')]
        self.assertFalse(HTML2mdConverter.is_tag_ignored("table", attrs))

        attrs = []
        self.assertFalse(HTML2mdConverter.is_tag_ignored("div", attrs))

    def test_title(self):
        self.assertEqual("---\ntitle: Recursos Física - Cinética\n---\n",
                         HTML2mdConverter.title("Recursos Física: Cinética"))

    def test_comment(self):
        self.assertEqual("[//]: # (This is a comment)",
                         HTML2mdConverter.comment("This is a comment"))
