from chronomits import Chronomits
from unittest.mock import patch
from unittest import mock
import unittest
import os

class TestChronomits(unittest.TestCase):

    def setUp(self):
        self.chronomit_mock = Chronomits(repositorio_local="caminho/ficticio", numero_de_commits="10")

    def tearDown(self):
        pass

    def test_obter_caminho_banner_retorna_caminho(self):
        # given
        banner_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "banner.sh"))
        self.chronomit_mock.obter_caminho_do_banner = mock.MagicMock(return_value=banner_path)

        # when
        actual_path = self.chronomit_mock.obter_caminho_do_banner()

        # then
        self.assertEqual(banner_path, actual_path)

    def test_verifica_argumentos_do_chronomit(self):
        with self.assertRaises(SystemExit) as cm:
            self.chronomit_mock.verifica_argumentos()

        self.assertEqual(cm.exception.code, 1)  # Confirma que sys.exit foi chamado com o código 1

    @mock.patch('subprocess.call')
    @mock.patch.object(Chronomits, 'obter_caminho_do_banner', return_value="/caminho/do/banner.sh")
    def test_exibe_banner_com_caminho_valido(self, mock_obter_caminho_do_banner, mock_subprocess_call):
        # when
        self.chronomit_mock.exibe_banner()

        # then
        mock_obter_caminho_do_banner.assert_called_once()
        mock_subprocess_call.assert_any_call(["chmod", "+x", "/caminho/do/banner.sh"])
        mock_subprocess_call.assert_any_call(["/caminho/do/banner.sh"])

    def test_verifica_existencia_repositorio_existente(self):
        # Dado que o atributo repositorio_local da instância tem um caminho fictício
        self.chronomit_mock.repositorio_local = "/caminho/ficticio/do/repositorio"

        # Mockando o os.path.exists para retornar True para este caminho fictício
        with patch("os.path.exists", return_value=True) as mock_exists:
            # A função deve retornar sem erros, pois estamos "simulando" que o diretório existe
            verifica_repositorio = self.chronomit_mock.verifica_existencia_repositorio()

            # Verificar se o os.path.exists foi chamado com o caminho fictício
            mock_exists.assert_called_with("/caminho/ficticio/do/repositorio")

    def test_verifica_existencia_repositorio_inexistente(self):
        with patch("os.path.exists", return_value=False):
            with self.assertRaises(SystemExit) as context:
                self.chronomit_mock.verifica_existencia_repositorio()

            self.assertEqual(context.exception.code, 1)  # Verifica se o código de saída é 1

if __name__ == '__main__':
    unittest.main()
