from chronomits import Chronomits
from unittest.mock import Mock
import unittest
import sys
import os

class TestChronomits(unittest.TestCase):

    def setUp(self):
        self.chronomit_mock = Mock(spec=Chronomits)

    def tearDown(self):
        pass

    def test_obter_caminho_banner_retorna_caminho(self):
        # given
        actual_path = self.chronomit_mock.obter_caminho_do_banner()
        banner_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "banner.sh"))
        
        # when
        self.chronomit_mock.obter_caminho_do_banner.return_value = banner_path
        actual_path = self.chronomit_mock.obter_caminho_do_banner()

        # then
        self.assertEqual(banner_path, actual_path)

    def test_verifica_argumentos(self):
        # given
        mock_argv = ["script.py", "/caminho/do/repositorio/local", "10"]
        sys.argv = mock_argv

        # when
        self.chronomit_mock.verifica_argumentos()

        # then
        self.assertEqual(3, len(sys.argv))


if __name__ == '__main__':
    unittest.main()