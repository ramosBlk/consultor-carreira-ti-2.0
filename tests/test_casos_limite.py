import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.engine import load_knowledge_base as carregar_base_conhecimento
from engine.engine import rank_careers as classificar_trilhas
from engine.roadmap import analisar_lacunas


class TesteCasosLimite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_conhecimento = carregar_base_conhecimento()
        cls.valor_minimo = cls.base_conhecimento["likert_scale"]["minimum"]
        cls.valor_maximo = cls.base_conhecimento["likert_scale"]["maximum"]

    def respostas_com_valor(self, valor):
        return {
            pergunta["id"]: valor
            for pergunta in self.base_conhecimento["questions"]
        }

    def test_perfil_ambiguo_mantem_dados_e_frontend_no_top_tres(self):
        respostas = self.respostas_com_valor(3)
        respostas.update(
            {
                "mathematics": 5,
                "data_analysis": 5,
                "artificial_intelligence": 5,
                "visual_design": 5,
                "user_experience": 5,
            }
        )

        ranking = classificar_trilhas(
            respostas,
            knowledge_base=self.base_conhecimento,
        )

        identificadores = [trilha.career_id for trilha in ranking]
        self.assertIn("data_science", identificadores)
        self.assertIn("frontend_ux", identificadores)
        self.assertGreater(ranking[0].compatibility_percent, ranking[1].compatibility_percent)

    def test_empate_parcial_preserva_ordem_das_trilhas_na_base(self):
        respostas = self.respostas_com_valor(3)
        respostas["mathematics"] = 5

        ranking = classificar_trilhas(
            respostas,
            knowledge_base=self.base_conhecimento,
        )

        self.assertEqual(
            [trilha.career_id for trilha in ranking],
            ["data_science", "backend", "frontend_ux"],
        )
        self.assertEqual(ranking[1].compatibility_percent, 50.0)
        self.assertEqual(ranking[2].compatibility_percent, 50.0)

    def test_extremos_da_escala_produzem_zero_e_cem_por_cento(self):
        ranking_minimo = classificar_trilhas(
            self.respostas_com_valor(self.valor_minimo),
            top_n=None,
            knowledge_base=self.base_conhecimento,
        )
        ranking_maximo = classificar_trilhas(
            self.respostas_com_valor(self.valor_maximo),
            top_n=None,
            knowledge_base=self.base_conhecimento,
        )

        self.assertTrue(
            all(trilha.compatibility_percent == 0 for trilha in ranking_minimo)
        )
        self.assertTrue(
            all(trilha.compatibility_percent == 100 for trilha in ranking_maximo)
        )

    def test_rejeita_tipo_pergunta_e_quantidade_de_resultados_invalidos(self):
        casos_invalidos = [
            ({"mathematics": True}, None, TypeError),
            ({"mathematics": 3.5}, None, TypeError),
            ({"pergunta_inexistente": 3}, None, ValueError),
            ({"mathematics": 3}, 0, ValueError),
        ]

        for respostas, quantidade, erro_esperado in casos_invalidos:
            with self.subTest(respostas=respostas, quantidade=quantidade):
                with self.assertRaises(erro_esperado):
                    classificar_trilhas(
                        respostas,
                        top_n=quantidade,
                        knowledge_base=self.base_conhecimento,
                    )

    def test_habilidades_no_nivel_junior_nao_criam_lacunas(self):
        trilha = next(
            trilha
            for trilha in self.base_conhecimento["career_paths"]
            if trilha["id"] == "backend"
        )
        conhecimentos = {
            habilidade["id"]: self.base_conhecimento["skill_scale"][
                "junior_target_level"
            ]
            for habilidade in trilha["junior_skills"]
        }

        lacunas = analisar_lacunas(
            "backend",
            conhecimentos,
            self.base_conhecimento,
        )

        self.assertEqual(lacunas, [])


if __name__ == "__main__":
    unittest.main()