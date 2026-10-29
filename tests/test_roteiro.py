import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.engine import load_knowledge_base as carregar_base_conhecimento
from engine.roadmap import analisar_lacunas, gerar_roadmap


class TesteRoadmap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_conhecimento = carregar_base_conhecimento()

    def test_lista_lacunas_por_prioridade_e_sinaliza_nivel_nao_informado(self):
        lacunas = analisar_lacunas(
            "backend",
            {
                "programming_fundamentals": 1,
                "backend_language": 3,
                "http_apis": 2,
                "relational_database": 4,
            },
            self.base_conhecimento,
        )

        self.assertEqual(
            [lacuna.identificador_habilidade for lacuna in lacunas],
            ["programming_fundamentals", "http_apis", "git_testing"],
        )
        self.assertTrue(lacunas[0].nivel_informado)
        self.assertFalse(lacunas[2].nivel_informado)
        self.assertEqual(lacunas[2].nivel_atual, 1)

    def test_nao_lista_habilidades_que_atingiram_o_alvo_junior(self):
        lacunas = analisar_lacunas(
            "backend",
            {"programming_fundamentals": 3, "backend_language": 5},
            self.base_conhecimento,
        )

        identificadores = {lacuna.identificador_habilidade for lacuna in lacunas}
        self.assertNotIn("programming_fundamentals", identificadores)
        self.assertNotIn("backend_language", identificadores)

    def test_monta_roadmap_com_recomendacoes_da_base_json(self):
        roteiro = gerar_roadmap("backend", {}, self.base_conhecimento)

        self.assertEqual(roteiro.nome_trilha, "Desenvolvimento Back-end")
        self.assertEqual(roteiro.tecnologias[0], "Python ou Java")
        self.assertTrue(roteiro.certificacoes)
        self.assertTrue(roteiro.projetos_portfolio)
        self.assertEqual(len(roteiro.lacunas), 5)

    def test_prioriza_tecnologias_das_lacunas_e_adapta_ritmo_ao_prazo(self):
        niveis = {
            "programming_fundamentals": 3,
            "backend_language": 3,
            "http_apis": 1,
            "relational_database": 3,
            "git_testing": 3,
        }

        roteiro = gerar_roadmap(
            "backend",
            niveis,
            self.base_conhecimento,
            career_timeline="Até 6 meses",
            weekly_study_hours=8,
        )

        self.assertEqual(roteiro.tecnologias[0], "HTTP e APIs REST")
        self.assertIn("Ritmo intensivo", roteiro.ritmo_sugerido)
        self.assertIn("8 h por semana", roteiro.ritmo_sugerido)
        self.assertTrue(roteiro.certificacoes)
        self.assertTrue(roteiro.projetos_portfolio)

    def test_personaliza_certificacao_e_projeto_conforme_gap(self):
        niveis = {
            "programming_fundamentals": 3,
            "backend_language": 3,
            "http_apis": 3,
            "relational_database": 1,
            "git_testing": 3,
        }

        roteiro = gerar_roadmap("backend", niveis, self.base_conhecimento)

        self.assertEqual(
            roteiro.certificacoes,
            ("Certificação introdutória de banco de dados, opcional",),
        )
        self.assertIn("SQL e banco de dados relacional", roteiro.projetos_portfolio[-1])

    def test_rejeita_prazo_e_disponibilidade_invalidos(self):
        with self.assertRaises(ValueError):
            gerar_roadmap(
                "backend",
                {},
                self.base_conhecimento,
                career_timeline="Prazo inválido",
            )

        with self.assertRaises(ValueError):
            gerar_roadmap(
                "backend",
                {},
                self.base_conhecimento,
                weekly_study_hours=0,
            )

    def test_rejeita_trilha_habilidade_e_nivel_invalidos(self):
        with self.assertRaises(ValueError):
            analisar_lacunas("trilha_inexistente", {}, self.base_conhecimento)

        with self.assertRaises(ValueError):
            analisar_lacunas("backend", {"habilidade_inexistente": 2}, self.base_conhecimento)

        with self.assertRaises(ValueError):
            analisar_lacunas("backend", {"backend_language": 6}, self.base_conhecimento)


if __name__ == "__main__":
    unittest.main()