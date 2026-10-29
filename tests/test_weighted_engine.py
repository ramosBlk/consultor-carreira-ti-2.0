'Mecanismo de teste ponderado'
'Ponderada'

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.engine import load_knowledge_base, rank_careers


class WeightedInferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.knowledge_base = load_knowledge_base()

    def test_returns_top_three_in_compatibility_order(self):
        ranking = rank_careers(
            {"logical_reasoning": 3, "visual_design": 3},
            knowledge_base=self.knowledge_base,
        )

        self.assertEqual(len(ranking), 3)
        self.assertGreaterEqual(
            ranking[0].compatibility_percent,
            ranking[1].compatibility_percent,
        )
        self.assertGreaterEqual(
            ranking[1].compatibility_percent,
            ranking[2].compatibility_percent,
        )

    def test_normalizes_weighted_answers_to_percent(self):
        ranking = rank_careers(
            {"mathematics": 5, "logical_reasoning": 1},
            top_n=None,
            knowledge_base=self.knowledge_base,
        )
        data_science = next(item for item in ranking if item.career_id == "data_science")

        self.assertEqual(data_science.compatibility_percent, 57.1)

    def test_applies_penalty_configured_in_knowledge_base(self):
        ranking = rank_careers(
            {"security": 5, "incident_response": 1},
            top_n=None,
            knowledge_base=self.knowledge_base,
        )
        cybersecurity = next(item for item in ranking if item.career_id == "cybersecurity")

        self.assertEqual(cybersecurity.compatibility_percent, 50.3)
        self.assertEqual(len(cybersecurity.penalty_reasons), 1)

    def test_work_preference_influences_ranking_without_replacing_affinity(self):
        answers = {
            question["id"]: 3 for question in self.knowledge_base["questions"]
        }
        affinity_ranking = rank_careers(
            answers,
            top_n=None,
            knowledge_base=self.knowledge_base,
        )
        objective_ranking = rank_careers(
            answers,
            top_n=None,
            knowledge_base=self.knowledge_base,
            objectives={
                "work_preference": "Manter sistemas e infraestrutura confiáveis"
            },
        )

        self.assertEqual(affinity_ranking[0].compatibility_percent, 50.0)
        self.assertEqual(objective_ranking[0].career_id, "devops_sre")
        self.assertEqual(objective_ranking[0].compatibility_percent, 60.0)

    def test_exploratory_preference_does_not_change_affinity_score(self):
        answers = {"logical_reasoning": 4}
        without_objective = rank_careers(
            answers, knowledge_base=self.knowledge_base
        )
        exploring = rank_careers(
            answers,
            knowledge_base=self.knowledge_base,
            objectives={"work_preference": "Ainda estou explorando"},
        )

        self.assertEqual(without_objective, exploring)

    def test_rejects_unknown_objectives_and_preferences(self):
        with self.assertRaises(ValueError):
            rank_careers(
                {"logical_reasoning": 3},
                knowledge_base=self.knowledge_base,
                objectives={"career_timeline": "Até 6 meses"},
            )

        with self.assertRaises(ValueError):
            rank_careers(
                {"logical_reasoning": 3},
                knowledge_base=self.knowledge_base,
                objectives={"work_preference": "Preferência inexistente"},
            )

    def test_rejects_empty_answers_and_values_outside_likert_scale(self):
        with self.assertRaises(ValueError):
            rank_careers({}, knowledge_base=self.knowledge_base)

        with self.assertRaises(ValueError):
            rank_careers(
                {"logical_reasoning": 6}, knowledge_base=self.knowledge_base
            )


if __name__ == "__main__":
    unittest.main()