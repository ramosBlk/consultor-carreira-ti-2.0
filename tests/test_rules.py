import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.facts import Usuario
from engine.questions import QUESTIONS
from engine.rules import MotorRegras
from models.careers import (
    BACKEND,
    CLOUD,
    CYBERSECURITY,
    DATA_ENGINEERING,
    DATA_SCIENCE,
    DEVOPS,
    FRONTEND,
    MOBILE,
    PRODUCT,
    QA,
)


class MotorRegrasTests(unittest.TestCase):
    def recomendar(self, respostas):
        motor = MotorRegras()
        motor.reset()
        motor.declare(Usuario(**respostas))
        motor.run()
        return motor

    def test_recomenda_carreira_para_perfis_representativos(self):
        casos = [
            (
                "back-end",
                {"linguagem": "Python", "atividade": "Criar APIs"},
                BACKEND,
            ),
            (
                "front-end",
                {"linguagem": "JavaScript", "atividade": "Criar Interfaces"},
                FRONTEND,
            ),
            (
                "ciência de dados",
                {
                    "matematica": "Alta",
                    "linguagem": "Python",
                    "inteligencia_artificial": "Sim",
                },
                DATA_SCIENCE,
            ),
            (
                "engenharia de dados",
                {
                    "atividade": "Analisar Dados",
                    "inteligencia_artificial": "Sim",
                    "banco_dados": "Sim",
                    "automacao": "Sim",
                },
                DATA_ENGINEERING,
            ),
            (
                "cibersegurança",
                {"atividade": "Segurança", "entrega": "Segurança"},
                CYBERSECURITY,
            ),
            (
                "DevOps",
                {"automacao": "Sim", "redes": "Sim"},
                DEVOPS,
            ),
            (
                "computação em nuvem",
                {"cloud": "Sim", "atividade": "Infraestrutura"},
                CLOUD,
            ),
            (
                "desenvolvimento mobile",
                {"mobile": "Sim", "atividade": "Aplicativos Mobile"},
                MOBILE,
            ),
            (
                "qualidade e testes",
                {"testes": "Sim", "automacao": "Sim"},
                QA,
            ),
            (
                "gestão de produtos",
                {"negocios": "Sim", "atividade": "Gestão de Produto"},
                PRODUCT,
            ),
        ]

        for perfil, respostas, carreira_esperada in casos:
            with self.subTest(perfil=perfil):
                motor = self.recomendar(respostas)

                self.assertEqual(motor.resultado, carreira_esperada)
                self.assertTrue(motor.justificativa)

    def test_nao_recomenda_carreira_sem_regra_compatível(self):
        motor = self.recomendar(
            {"atividade": "Testes", "negocios": "Não"}
        )

        self.assertIsNone(motor.resultado)
        self.assertEqual(motor.justificativa, [])

    def test_opcoes_das_perguntas_sao_validas_e_nao_vazias(self):
        self.assertTrue(QUESTIONS)
        for pergunta, opcoes in QUESTIONS.items():
            with self.subTest(pergunta=pergunta):
                self.assertTrue(opcoes)
                self.assertEqual(len(opcoes), len(set(opcoes)))


if __name__ == "__main__":
    unittest.main()
