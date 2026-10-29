from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from engine.engine import load_knowledge_base as carregar_base_conhecimento


@dataclass(frozen=True)
class LacunaCompetencia:
    identificador_habilidade: str
    nome_habilidade: str
    nivel_atual: int
    nivel_alvo: int
    diferenca: int
    nivel_informado: bool
    prioridade: int


@dataclass(frozen=True)
class PlanoEstudos:
    identificador_trilha: str
    nome_trilha: str
    lacunas: tuple[LacunaCompetencia, ...]
    tecnologias: tuple[str, ...]
    certificacoes: tuple[str, ...]
    projetos_portfolio: tuple[str, ...]
    ritmo_sugerido: str | None


def analisar_lacunas(
    identificador_trilha: str,
    conhecimentos: Mapping[str, int],
    base_conhecimento: Mapping[str, Any] | None = None,
) -> list[LacunaCompetencia]:
    """Compara os conhecimentos informados com o nível júnior da trilha."""
    base = (
        base_conhecimento
        if base_conhecimento is not None
        else carregar_base_conhecimento()
    )
    trilha = _obter_trilha(identificador_trilha, base)
    nivel_minimo = base["skill_scale"]["minimum"]
    nivel_maximo = base["skill_scale"]["maximum"]
    nivel_alvo = base["skill_scale"]["junior_target_level"]

    if not isinstance(conhecimentos, Mapping):
        raise TypeError("Os conhecimentos devem ser informados em um mapeamento.")

    habilidades_conhecidas = {
        habilidade["id"]
        for item_trilha in base["career_paths"]
        for habilidade in item_trilha["junior_skills"]
    }
    habilidades_desconhecidas = set(conhecimentos) - habilidades_conhecidas
    if habilidades_desconhecidas:
        raise ValueError(
            "Habilidades desconhecidas: "
            + ", ".join(sorted(habilidades_desconhecidas))
        )

    for identificador_habilidade, nivel in conhecimentos.items():
        if isinstance(nivel, bool) or not isinstance(nivel, int):
            raise TypeError(
                f"O nível de '{identificador_habilidade}' deve ser um inteiro."
            )
        if not nivel_minimo <= nivel <= nivel_maximo:
            raise ValueError(
                f"O nível de '{identificador_habilidade}' deve estar entre "
                f"{nivel_minimo} e {nivel_maximo}."
            )

    lacunas = []
    for habilidade in trilha["junior_skills"]:
        nivel_informado = habilidade["id"] in conhecimentos
        nivel_atual = conhecimentos.get(habilidade["id"], nivel_minimo)
        diferenca = nivel_alvo - nivel_atual
        if diferenca > 0:
            lacunas.append(
                LacunaCompetencia(
                    identificador_habilidade=habilidade["id"],
                    nome_habilidade=habilidade["name"],
                    nivel_atual=nivel_atual,
                    nivel_alvo=nivel_alvo,
                    diferenca=diferenca,
                    nivel_informado=nivel_informado,
                    prioridade=habilidade["priority"],
                )
            )

    lacunas.sort(key=lambda lacuna: lacuna.prioridade)
    return lacunas


def gerar_roadmap(
    identificador_trilha: str,
    conhecimentos: Mapping[str, int],
    base_conhecimento: Mapping[str, Any] | None = None,
    career_timeline: str | None = None,
    weekly_study_hours: int | None = None,
) -> PlanoEstudos:
    """Monta o plano da trilha usando lacunas e recomendações do JSON."""
    base = (
        base_conhecimento
        if base_conhecimento is not None
        else carregar_base_conhecimento()
    )
    trilha = _obter_trilha(identificador_trilha, base)
    lacunas = analisar_lacunas(identificador_trilha, conhecimentos, base)
    recomendacoes = trilha["roadmap"]
    tecnologia_por_habilidade = recomendacoes.get("technology_by_skill", {})
    tecnologias_priorizadas = []
    for lacuna in lacunas:
        for tecnologia in tecnologia_por_habilidade.get(
            lacuna.identificador_habilidade, []
        ):
            if tecnologia not in tecnologias_priorizadas:
                tecnologias_priorizadas.append(tecnologia)
    tecnologias_priorizadas.extend(
        tecnologia
        for tecnologia in recomendacoes["technologies"]
        if tecnologia not in tecnologias_priorizadas
    )
    certificacoes_personalizadas = []
    certificacoes_por_habilidade = recomendacoes.get(
        "certification_by_skill", {}
    )
    for lacuna in lacunas:
        certificacao = certificacoes_por_habilidade.get(
            lacuna.identificador_habilidade
        )
        if certificacao and certificacao not in certificacoes_personalizadas:
            certificacoes_personalizadas.append(certificacao)
    if not certificacoes_personalizadas:
        certificacoes_personalizadas = recomendacoes["certifications"]

    projetos_portfolio = list(recomendacoes["portfolio_projects"])
    modelo_projeto = base.get("portfolio_gap_template")
    if lacunas and modelo_projeto:
        habilidades_prioritarias = ", ".join(
            lacuna.nome_habilidade for lacuna in lacunas
        )
        projetos_portfolio.append(
            modelo_projeto.format(skills=habilidades_prioritarias)
        )

    ritmo_sugerido = None
    if career_timeline is not None:
        orientacao_prazo = base.get("timeline_guidance", {}).get(career_timeline)
        if orientacao_prazo is None:
            raise ValueError(f"Prazo de carreira desconhecido: {career_timeline}")
        ritmo_sugerido = orientacao_prazo
    if weekly_study_hours is not None:
        if isinstance(weekly_study_hours, bool) or not isinstance(
            weekly_study_hours, int
        ):
            raise TypeError("As horas semanais de estudo devem ser um inteiro.")
        hours_field = next(
            (
                field
                for step in base.get("wizard_steps", [])
                for field in step.get("fields", [])
                if field.get("id") == "weekly_study_hours"
            ),
            None,
        )
        if hours_field is None:
            raise ValueError("A base não define os limites de horas semanais.")
        minimum = hours_field["minimum"]
        maximum = hours_field["maximum"]
        if not minimum <= weekly_study_hours <= maximum:
            raise ValueError(
                f"As horas semanais de estudo devem estar entre {minimum} e {maximum}."
            )
        dedicacao = f"Dedicação informada: {weekly_study_hours} h por semana."
        ritmo_sugerido = (
            f"{ritmo_sugerido} {dedicacao}"
            if ritmo_sugerido
            else dedicacao
        )

    return PlanoEstudos(
        identificador_trilha=trilha["id"],
        nome_trilha=trilha["name"],
        lacunas=tuple(lacunas),
        tecnologias=tuple(tecnologias_priorizadas),
        certificacoes=tuple(certificacoes_personalizadas),
        projetos_portfolio=tuple(projetos_portfolio),
        ritmo_sugerido=ritmo_sugerido,
    )


def _obter_trilha(
    identificador_trilha: str,
    base_conhecimento: Mapping[str, Any],
) -> Mapping[str, Any]:
    for trilha in base_conhecimento["career_paths"]:
        if trilha["id"] == identificador_trilha:
            return trilha
    raise ValueError(f"Trilha desconhecida: {identificador_trilha}")