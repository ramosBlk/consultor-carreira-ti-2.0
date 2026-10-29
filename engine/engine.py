from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CareerCompatibility:
    career_id: str
    career_name: str
    compatibility_percent: float
    matched_questions: tuple[str, ...]
    penalty_reasons: tuple[str, ...]


def load_knowledge_base(path: str | Path | None = None) -> dict[str, Any]:
    """Load and validate the JSON knowledge base."""
    source = (
        Path(path)
        if path is not None
        else Path(__file__).resolve().parents[1] / "regras_carreiras.json"
    )

    with source.open(encoding="utf-8") as knowledge_file:
        knowledge_base = json.load(knowledge_file)

    _validate_knowledge_base(knowledge_base)
    return knowledge_base


def rank_careers(
    answers: Mapping[str, int],
    top_n: int | None = 3,
    knowledge_base: Mapping[str, Any] | None = None,
    objectives: Mapping[str, str] | None = None,
) -> list[CareerCompatibility]:
    """Rank careers by weighted affinity and work preference, with configured penalties."""
    base = knowledge_base if knowledge_base is not None else load_knowledge_base()
    _validate_knowledge_base(base)

    if not isinstance(answers, Mapping):
        raise TypeError("As respostas devem ser fornecidas como um mapeamento.")
    if not answers:
        raise ValueError("Informe ao menos uma resposta para calcular a compatibilidade.")
    if objectives is None:
        objectives = {}
    if not isinstance(objectives, Mapping):
        raise TypeError("Os objetivos devem ser fornecidos como um mapeamento.")
    unknown_objectives = set(objectives) - {"work_preference"}
    if unknown_objectives:
        raise ValueError(
            "Objetivos desconhecidos: " + ", ".join(sorted(unknown_objectives))
        )
    work_preference = objectives.get("work_preference")
    if work_preference is not None:
        if not isinstance(work_preference, str):
            raise TypeError("A preferência de trabalho deve ser um texto.")
        valid_preferences = {
            option
            for step in base.get("wizard_steps", [])
            for field in step.get("fields", [])
            if field.get("id") == "work_preference"
            for option in field.get("options", [])
        }
        if work_preference not in valid_preferences:
            raise ValueError("A preferência de trabalho não é uma opção válida.")
    if top_n is not None and (
        isinstance(top_n, bool) or not isinstance(top_n, int) or top_n < 1
    ):
        raise ValueError("top_n deve ser um inteiro positivo ou None.")

    question_ids = {question["id"] for question in base["questions"]}
    unknown_questions = set(answers) - question_ids
    if unknown_questions:
        raise ValueError(
            "Perguntas desconhecidas: " + ", ".join(sorted(unknown_questions))
        )

    scale = base["likert_scale"]
    minimum = scale["minimum"]
    maximum = scale["maximum"]
    for question_id, value in answers.items():
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"A resposta '{question_id}' deve ser um inteiro.")
        if not minimum <= value <= maximum:
            raise ValueError(
                f"A resposta '{question_id}' deve estar entre {minimum} e {maximum}."
            )

    question_prompts = {
        question["id"]: question["prompt"] for question in base["questions"]
    }
    ranked: list[CareerCompatibility] = []

    for career in base["career_paths"]:
        weighted_answers = [
            (question_id, answers[question_id], weight)
            for question_id, weight in career["question_weights"].items()
            if question_id in answers
        ]
        total_weight = sum(weight for _, _, weight in weighted_answers)

        if total_weight:
            weighted_score = sum(
                ((value - minimum) / (maximum - minimum)) * weight
                for _, value, weight in weighted_answers
            ) / total_weight
        else:
            weighted_score = 0.0

        preference_score = career.get("work_preference_scores", {}).get(
            work_preference
        )
        if preference_score is not None:
            objective_weight = base.get("objective_fit_weight", 0.0)
            weighted_score = (
                weighted_score * (1 - objective_weight)
                + preference_score * objective_weight
            )

        penalty_reasons = []
        for penalty in base.get("fit_penalties", []):
            if career["id"] not in penalty["career_ids"]:
                continue
            if all(_condition_matches(condition, answers) for condition in penalty["when"]):
                weighted_score *= 1 - penalty["penalty"]
                penalty_reasons.append(penalty["reason"])

        ranked.append(
            CareerCompatibility(
                career_id=career["id"],
                career_name=career["name"],
                compatibility_percent=round(weighted_score * 100, 1),
                matched_questions=tuple(
                    question_prompts[question_id]
                    for question_id, _, _ in weighted_answers
                ),
                penalty_reasons=tuple(penalty_reasons),
            )
        )

    ranked.sort(key=lambda result: result.compatibility_percent, reverse=True)
    return ranked if top_n is None else ranked[:top_n]


def _condition_matches(condition: Mapping[str, Any], answers: Mapping[str, int]) -> bool:
    question_id = condition["question_id"]
    if question_id not in answers:
        return False

    value = answers[question_id]
    operator = condition["operator"]
    threshold = condition["value"]
    if operator == "less_than_or_equal":
        return value <= threshold
    if operator == "less_than":
        return value < threshold
    if operator == "greater_than_or_equal":
        return value >= threshold
    if operator == "greater_than":
        return value > threshold
    if operator == "equals":
        return value == threshold
    raise ValueError(f"Operador de penalidade não suportado: {operator}")


def _validate_knowledge_base(knowledge_base: Mapping[str, Any]) -> None:
    if not isinstance(knowledge_base, Mapping):
        raise ValueError("A base de conhecimento deve ser um objeto JSON.")

    try:
        scale = knowledge_base["likert_scale"]
        minimum = scale["minimum"]
        maximum = scale["maximum"]
        questions = knowledge_base["questions"]
        careers = knowledge_base["career_paths"]
    except (KeyError, TypeError) as error:
        raise ValueError("A base não contém a estrutura mínima para inferência.") from error

    if minimum >= maximum:
        raise ValueError("A escala Likert deve ter mínimo menor que o máximo.")

    question_ids = [question.get("id") for question in questions]
    if not question_ids or len(question_ids) != len(set(question_ids)):
        raise ValueError("A base deve conter perguntas com identificadores únicos.")

    career_ids = [career.get("id") for career in careers]
    if not career_ids or len(career_ids) != len(set(career_ids)):
        raise ValueError("A base deve conter trilhas com identificadores únicos.")

    question_id_set = set(question_ids)
    for career in careers:
        weights = career.get("question_weights", {})
        if not isinstance(weights, Mapping):
            raise ValueError(f"Os pesos da trilha '{career.get('id')}' são inválidos.")
        unknown_weights = set(weights) - question_id_set
        if unknown_weights:
            raise ValueError(
                f"Pesos sem perguntas correspondentes: {', '.join(sorted(unknown_weights))}"
            )
        if any(
            isinstance(weight, bool)
            or not isinstance(weight, (int, float))
            or weight < 0
            for weight in weights.values()
        ):
            raise ValueError(f"Os pesos da trilha '{career.get('id')}' são inválidos.")

        skills = career.get("junior_skills", [])
        skill_ids = {skill.get("id") for skill in skills}
        roadmap = career.get("roadmap", {})
        technology_map = roadmap.get("technology_by_skill", {})
        certification_map = roadmap.get("certification_by_skill", {})
        if not isinstance(technology_map, Mapping):
            raise ValueError(
                f"O mapa de tecnologias da trilha '{career.get('id')}' é inválido."
            )
        if not isinstance(certification_map, Mapping):
            raise ValueError(
                f"O mapa de certificações da trilha '{career.get('id')}' é inválido."
            )
        if not set(technology_map).issubset(skill_ids):
            raise ValueError(
                f"O mapa de tecnologias da trilha '{career.get('id')}' "
                "referencia uma habilidade inexistente."
            )
        if not set(certification_map).issubset(skill_ids) or any(
            not isinstance(certification, str) or not certification.strip()
            for certification in certification_map.values()
        ):
            raise ValueError(
                f"O mapa de certificações da trilha '{career.get('id')}' é inválido."
            )
        technologies = roadmap.get("technologies", [])
        if any(
            not isinstance(items, list)
            or any(item not in technologies for item in items)
            for items in technology_map.values()
        ):
            raise ValueError(
                f"O mapa de tecnologias da trilha '{career.get('id')}' "
                "referencia uma tecnologia inexistente."
            )

    career_id_set = set(career_ids)
    objective_weight = knowledge_base.get("objective_fit_weight", 0.0)
    if (
        isinstance(objective_weight, bool)
        or not isinstance(objective_weight, (int, float))
        or not 0 <= objective_weight <= 1
    ):
        raise ValueError("O peso dos objetivos deve estar entre 0 e 1.")

    valid_preferences = {
        option
        for step in knowledge_base.get("wizard_steps", [])
        for field in step.get("fields", [])
        if field.get("id") == "work_preference"
        for option in field.get("options", [])
    }
    valid_timelines = {
        option
        for step in knowledge_base.get("wizard_steps", [])
        for field in step.get("fields", [])
        if field.get("id") == "career_timeline"
        for option in field.get("options", [])
    }
    timeline_guidance = knowledge_base.get("timeline_guidance", {})
    if not isinstance(timeline_guidance, Mapping):
        raise ValueError("As orientações de prazo são inválidas.")
    if not set(timeline_guidance).issubset(valid_timelines) or any(
        not isinstance(guidance, str) or not guidance.strip()
        for guidance in timeline_guidance.values()
    ):
        raise ValueError("Uma orientação referencia um prazo inválido.")
    portfolio_gap_template = knowledge_base.get("portfolio_gap_template")
    if portfolio_gap_template is not None and (
        not isinstance(portfolio_gap_template, str)
        or "{skills}" not in portfolio_gap_template
    ):
        raise ValueError("O modelo de projeto para lacunas é inválido.")

    for career in careers:
        preference_scores = career.get("work_preference_scores", {})
        if not isinstance(preference_scores, Mapping):
            raise ValueError(
                f"As pontuações de preferência da trilha '{career.get('id')}' são inválidas."
            )
        if not set(preference_scores).issubset(valid_preferences):
            raise ValueError("Uma pontuação referencia uma preferência inexistente.")
        if any(
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 1
            for score in preference_scores.values()
        ):
            raise ValueError(
                f"As pontuações de preferência da trilha '{career.get('id')}' são inválidas."
            )

    for penalty in knowledge_base.get("fit_penalties", []):
        for condition in penalty.get("when", []):
            if condition.get("question_id") not in question_id_set:
                raise ValueError("A penalidade referencia uma pergunta inexistente.")
        if not set(penalty.get("career_ids", [])).issubset(career_id_set):
            raise ValueError("A penalidade referencia uma trilha inexistente.")
        amount = penalty.get("penalty")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not 0 <= amount <= 1:
            raise ValueError("A penalidade deve estar entre 0 e 1.")