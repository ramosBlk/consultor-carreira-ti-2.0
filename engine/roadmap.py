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

    return PlanoEstudos(
        identificador_trilha=trilha["id"],
        nome_trilha=trilha["name"],
        lacunas=tuple(lacunas),
        tecnologias=tuple(recomendacoes["technologies"]),
        certificacoes=tuple(recomendacoes["certifications"]),
        projetos_portfolio=tuple(recomendacoes["portfolio_projects"]),
    )


def _obter_trilha(
    identificador_trilha: str,
    base_conhecimento: Mapping[str, Any],
) -> Mapping[str, Any]:
    for trilha in base_conhecimento["career_paths"]:
        if trilha["id"] == identificador_trilha:
            return trilha
    raise ValueError(f"Trilha desconhecida: {identificador_trilha}")