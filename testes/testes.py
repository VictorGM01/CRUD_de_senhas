from unittest import TestCase

from CRUD.main import insere_valores, exclui_valores, atualiza_valores
from CRUD.excecoes import DelecaoInvalida


class TesteCrud(TestCase):

    # define cenário de testes
    def setUp(self) -> None:
        self.senha = "123456789"
        self.programa = "github"

    def test_deve_inserir_uma_nova_senha_quando_a_funcao_insere_valores_for_chamada(self):
        insere_valores(self.programa, self.senha)
        insere_valores('Facebook', '123456')

    def test_deve_excluir_uma_senha_quando_a_funcao_exclui_valores_for_chamada(self):
        exclui_valores(self.programa)

    def test_nao_deve_permitir_delecao_quando_o_programa_nao_for_encontrado(self):
        with self.assertRaises(DelecaoInvalida):
            exclui_valores('SATURNO')
            exclui_valores(3)

    def test_deve_permitir_atualizacao_de_senha_quando_a_funcao_atualiza_valores_for_chamada(self):
        atualiza_valores(self.programa, '141598')
