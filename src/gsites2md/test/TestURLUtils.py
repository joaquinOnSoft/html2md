import os
from unittest import TestCase

from gsites2md.URLUtils import URLUtils


class TestURLUtils(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        self.base_path += "/../../../resources/"

    def test_is_html(self):
        path = self.base_path + "test.html"
        self.assertTrue(URLUtils.is_html(path))

        path = self.base_path + "fiquipedia.es/recursos/2017-06-23-LogoFiquipedia.png"
        self.assertFalse(URLUtils.is_html(path))

    def test_is_friendly_url(self):
        path = self.base_path + "fiquipedia.es/recursos/2017-06-23-LogoFiquipedia.png"
        self.assertFalse(URLUtils.is_friendly_url(path))

        path = self.base_path + "fiquipedia.es/recursos/FiquipediaQR.png?height=320&width=320"
        self.assertFalse(URLUtils.is_friendly_url(path))

        path = self.base_path + "test"
        self.assertTrue(URLUtils.is_friendly_url(path))

    def test_is_twitter_stats_url(self):
        self.assertTrue(URLUtils.is_twitter_status_url("https://twitter.com/CIAandPatri/status/1035502202809450496"))
        self.assertFalse(URLUtils.is_twitter_status_url("https://youtu.be/MJF0dbZCVgQ"))

    def test_is_youtube_video_url(self):
        self.assertTrue(URLUtils.is_youtube_video_url("https://www.youtube.com/watch?v=MJF0dbZCVgQ"))
        self.assertTrue(URLUtils.is_youtube_video_url("https://youtu.be/MJF0dbZCVgQ"))

    def test_is_not_a_youtube_video_url(self):
        self.assertFalse(URLUtils.is_youtube_video_url("https://fiquipedia.es"))
        self.assertFalse(URLUtils.is_youtube_video_url("http://www.cece.gva.es/univ/es/PAU_informacion_general.htm"))

    def test_is_youtube_video_url(self):
        self.assertEqual("MJF0dbZCVgQ", URLUtils.get_youtube_video_id("https://www.youtube.com/watch?v=MJF0dbZCVgQ"))

    def test_check_url_never_ends(self):
        self.assertFalse(URLUtils.check_url_exists("http://www.upm.es/FuturosEstudiantes/Ingresar/Acceso/EvAU"))

    def test_check_url_exists(self):
        self.assertTrue(URLUtils.check_url_exists("https://twitter.com/CIAandPatri/status/1035502202809450496"))
        self.assertFalse(URLUtils.check_url_exists("http://www.selectividad.profesores.net/"))
        self.assertTrue(URLUtils.check_url_exists("http://www.selectividad.tv/"))
        self.assertFalse(URLUtils.check_url_exists("http://www.selectividadonline.com/"))
        self.assertFalse(URLUtils.check_url_exists("http://graviton.blogspot.com.es/p/examenes-selectividad.html"))
        self.assertFalse(URLUtils.check_url_exists("http://graviton.blogspot.com.es/p/examenes-selectividad.html"))
        self.assertTrue(URLUtils.check_url_exists("http://fisquim.torrealmirante.net/selectividad.html"))
        self.assertFalse(URLUtils.check_url_exists("https://www.uc3m.es/ss/Satellite/"
                                                   "Grado/es/TextoDosColumnas/1371215758452/"))
        self.assertFalse(URLUtils.check_url_exists("http://www.mecd.gob.es/educacion-mecd/areas-educacion/"
                                                   "universidades/educacion-superior-universitaria/legislacion/"
                                                   "acceso-admision.html"))
        self.assertFalse(URLUtils.check_url_exists("http://www.mecd.gob.es/educacion-mecd/areas-educacion/"
                                                   "sistema-educativo/ensenanzas/bachillerato/"
                                                   "opciones-despues-bachillerato/pau.html"))
        self.assertFalse(URLUtils.check_url_exists("http://www.cece.gva.es/univ/docs/PAU_Guia_2009_2010_cas.pdf"))
