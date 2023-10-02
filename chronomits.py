import subprocess
import datetime
import random
import sys
import os

class Chronomits:
    def __init__(self, repositorio_local, numero_de_commits):
        self.repositorio_local = repositorio_local
        self.numero_de_commits = int(numero_de_commits)

    def obter_caminho_do_banner(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        banner_filename = "banner.sh"
        banner_path = os.path.join(script_directory, banner_filename)

        if os.path.exists(banner_path):
            return banner_path
        else:
            return None

    def verifica_argumentos(self):
        if len(sys.argv) != 3:
            print("Uso: python script.py /caminho/do/repositorio/local numero_de_commits")
            sys.exit(1)

    def verifica_existencia_repositorio(self):
        if not os.path.exists(self.repositorio_local):
            print(f"O diretório {self.repositorio_local} não existe.")
            sys.exit(1)

    def converte_numero_commits(self, numero_de_commits): # funcao sem teste unitário, sempre dá erro e sem possibilidade de mock
        try:
            return int(numero_de_commits)
        except ValueError:
            print("O número de commits deve ser um valor inteiro.")
            sys.exit(1)
            return 0

    def exibe_banner(self):
        banner_path = self.obter_caminho_do_banner()
        if banner_path:
            try:
                subprocess.call(["chmod", "+x", banner_path])
                subprocess.call([banner_path])
                return True
            except Exception as e:
                print(f"Erro ao exibir o banner: {e}")
                return False
        return False

    def cria_commits(self):
        os.chdir(self.repositorio_local)

        if not os.path.exists('README.md' ):
            with open('README.md', 'w') as readme:
                readme.write('Arquivo README\n\nEste é o conteúdo inicial do README.')

        for i in range(self.numero_de_commits):
            self.exibe_banner()
            # Gera uma data aleatória no passado
            data_commit = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))

            # Cria um arquivo README temporário com uma msg de commit
            with open('README.md', 'w') as readme:
                readme.write(f'Commit em {data_commit}\n\nConteúdo do commit {i}')

            subprocess.call(['git', 'add', 'README.md'])
            subprocess.call(['git', 'commit', '--date', data_commit.strftime('%Y-%m-%dT%H:%M:%S%z'), '-m', f'Commit em {data_commit}'])

        subprocess.call(['git', 'push', 'origin', 'main'])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py /caminho/do/repositorio/local numero_de_commits")
        sys.exit(1)

    repositorio_local = sys.argv[1]
    numero_de_commits = sys.argv[2]

    script = Chronomits(repositorio_local, numero_de_commits)
    script.verifica_argumentos()
    script.verifica_existencia_repositorio()
    script.converte_numero_commits(sys.argv[2])
    script.cria_commits()
