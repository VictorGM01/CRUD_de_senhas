from unittest import TestCase

from CRUD.main import insere_valores, exclui_valores


class TesteCrud(TestCase):

    # define cenário de testes
    def setUp(self) -> None:
        self.senha = "123456789"
        self.programa = "github"

    def test_deve_inserir_uma_nova_senha_quando_a_funcao_insere_valores_for_chamada(self):
        insere_valores(self.programa, self.senha)

    def test_deve_excluir_uma_senha_quando_a_funcao_exclui_valores_for_chamada(self):
        exclui_valores(self.programa)
