from __future__ import annotations

from typing import Any

import streamlit as st

from engine.engine import load_knowledge_base as carregar_base_conhecimento
from engine.engine import rank_careers as classificar_trilhas
from engine.roadmap import gerar_roadmap


st.set_page_config(
    page_title="Consultor de Carreiras em TI",
    page_icon="🧭",
    layout="wide",
)

base_conhecimento = carregar_base_conhecimento()
etapas = base_conhecimento["wizard_steps"]
perguntas_por_id = {
    pergunta["id"]: pergunta for pergunta in base_conhecimento["questions"]
}
rotulos_afinidade = base_conhecimento["likert_scale"]["labels"]
escala_competencias = base_conhecimento["skill_scale"]

st.session_state.setdefault("etapa_atual", 0)
st.session_state.setdefault("perfil_pessoal", {})
st.session_state.setdefault("respostas_afinidades", {})
st.session_state.setdefault("objetivos_carreira", {})
st.session_state.setdefault("competencias_por_trilha", {})
st.session_state.setdefault("trilha_escolhida", None)
st.session_state.setdefault("diagnostico_concluido", False)


def _renderizar_campo(campo: dict[str, Any], grupo: str) -> Any:
    dados_persistidos = st.session_state[grupo]
    identificador = campo["id"]
    chave_widget = f"widget_{grupo}_{identificador}"

    if chave_widget not in st.session_state:
        if identificador in dados_persistidos:
            st.session_state[chave_widget] = dados_persistidos[identificador]
        elif campo["type"] == "choice":
            st.session_state[chave_widget] = campo["options"][0]
        else:
            st.session_state[chave_widget] = campo["minimum"]

    if campo["type"] == "choice":
        valor = st.selectbox(
            campo["label"],
            campo["options"],
            key=chave_widget,
        )
    else:
        valor = st.number_input(
            campo["label"],
            min_value=campo["minimum"],
            max_value=campo["maximum"],
            step=1,
            key=chave_widget,
        )

    dados_persistidos[identificador] = valor
    return valor


def _obter_respostas_afinidades() -> dict[str, int]:
    return dict(st.session_state["respostas_afinidades"])


def _mostrar_resultado() -> None:
    respostas = _obter_respostas_afinidades()
    objetivo = st.session_state["objetivos_carreira"]
    perfil = st.session_state["perfil_pessoal"]
    trilhas_recomendadas = classificar_trilhas(
        respostas,
        top_n=3,
        knowledge_base=base_conhecimento,
        objectives={"work_preference": objetivo.get("work_preference")},
    )
    trilha_escolhida = st.session_state["trilha_escolhida"]
    competencias = st.session_state["competencias_por_trilha"].get(
        trilha_escolhida, {}
    )
    roteiro = gerar_roadmap(
        trilha_escolhida,
        competencias,
        base_conhecimento,
        career_timeline=objetivo.get("career_timeline"),
        weekly_study_hours=perfil.get("weekly_study_hours"),
    )

    st.header("Seu mapa de compatibilidade")
    st.bar_chart(
        data={
            "Trilha": [trilha.career_name for trilha in trilhas_recomendadas],
            "Compatibilidade (%)": [
                trilha.compatibility_percent for trilha in trilhas_recomendadas
            ],
        },
        x="Trilha",
        y="Compatibilidade (%)",
        horizontal=True,
    )

    colunas = st.columns(len(trilhas_recomendadas))
    for posicao, (coluna, trilha) in enumerate(
        zip(colunas, trilhas_recomendadas), start=1
    ):
        with coluna:
            st.metric(
                f"{posicao}º lugar · {trilha.career_name}",
                f"{trilha.compatibility_percent:.1f}%",
            )

    with st.expander("Ver fatores considerados no ranking"):
        if objetivo.get("work_preference") != "Ainda estou explorando":
            st.caption(
                f"Preferência de trabalho considerada: "
                f"{objetivo['work_preference']} "
                f"(peso de {base_conhecimento['objective_fit_weight'] * 100:.0f}% "
                "na compatibilidade)."
            )
        for trilha in trilhas_recomendadas:
            st.markdown(f"**{trilha.career_name}**")
            for pergunta in trilha.matched_questions:
                st.write(f"- {pergunta}")
            for motivo in trilha.penalty_reasons:
                st.caption(f"Ajuste aplicado: {motivo}")

    st.divider()
    st.subheader(f"Plano para {roteiro.nome_trilha}")
    st.caption(
        f"{objetivo['work_preference']} · "
        f"{objetivo['career_timeline']} · "
        f"{perfil['weekly_study_hours']} h de estudo por semana"
    )
    if roteiro.ritmo_sugerido:
        st.info(roteiro.ritmo_sugerido)

    st.markdown("#### Lacunas prioritárias para o nível júnior")
    if roteiro.lacunas:
        for lacuna in roteiro.lacunas:
            origem_nivel = (
                "informado"
                if lacuna.nivel_informado
                else "estimado como iniciante"
            )
            st.write(
                f"**{lacuna.prioridade}. {lacuna.nome_habilidade}** · "
                f"nível {lacuna.nivel_atual} ({origem_nivel}) → "
                f"nível {lacuna.nivel_alvo}"
            )
            st.progress(
                min(lacuna.nivel_atual / lacuna.nivel_alvo, 1.0),
                text=f"Distância até o nível-alvo: {lacuna.diferenca}",
            )
    else:
        st.success("As competências avaliadas já atingiram o nível júnior definido.")

    coluna_tecnologias, coluna_certificacoes = st.columns(2)
    with coluna_tecnologias:
        st.markdown("#### Tecnologias e tópicos")
        for tecnologia in roteiro.tecnologias:
            st.write(f"- {tecnologia}")
    with coluna_certificacoes:
        st.markdown("#### Certificações sugeridas")
        for certificacao in roteiro.certificacoes:
            st.write(f"- {certificacao}")

    st.markdown("#### Projeto de portfólio")
    for projeto in roteiro.projetos_portfolio:
        st.write(f"- {projeto}")

    if st.button("Recomeçar diagnóstico", key="reiniciar_diagnostico"):
        st.session_state.clear()
        st.rerun()


st.title("Consultor de Carreiras em TI")
st.caption("Compatibilidade por afinidades, lacunas de competências e plano de estudo.")

if st.session_state["diagnostico_concluido"]:
    _mostrar_resultado()
else:
    etapa_atual = st.session_state["etapa_atual"]
    st.progress((etapa_atual + 1) / len(etapas))
    st.caption(f"Etapa {etapa_atual + 1} de {len(etapas)} · {etapas[etapa_atual]['title']}")
    st.subheader(etapas[etapa_atual]["title"])

    if etapa_atual == 0:
        st.write("Conte um pouco sobre seu momento e sua disponibilidade.")
        for campo in etapas[0]["fields"]:
            _renderizar_campo(campo, "perfil_pessoal")

    elif etapa_atual == 1:
        st.write("Avalie cada afinidade de 1 a 5.")
        st.caption(
            "1 · Nenhuma afinidade     2 · Pouca     3 · Moderada     "
            "4 · Muita     5 · Total"
        )
        colunas = st.columns(2)
        minimo = base_conhecimento["likert_scale"]["minimum"]
        maximo = base_conhecimento["likert_scale"]["maximum"]
        valor_inicial = (minimo + maximo) // 2

        for indice, identificador in enumerate(etapas[1]["question_ids"]):
            pergunta = perguntas_por_id[identificador]
            chave_widget = f"widget_afinidade_{identificador}"
            if chave_widget not in st.session_state:
                st.session_state[chave_widget] = st.session_state[
                    "respostas_afinidades"
                ].get(identificador, valor_inicial)

            with colunas[indice % len(colunas)]:
                valor = st.slider(
                    pergunta["prompt"],
                    min_value=minimo,
                    max_value=maximo,
                    step=1,
                    key=chave_widget,
                )
            st.session_state["respostas_afinidades"][identificador] = valor

    else:
        st.write("Defina seus objetivos e avalie as habilidades da trilha escolhida.")
        for campo in etapas[2]["fields"]:
            _renderizar_campo(campo, "objetivos_carreira")

        trilhas_recomendadas = classificar_trilhas(
            _obter_respostas_afinidades(),
            top_n=3,
            knowledge_base=base_conhecimento,
            objectives={
                "work_preference": st.session_state["objetivos_carreira"].get(
                    "work_preference"
                )
            },
        )
        opcoes_trilhas = [trilha.career_id for trilha in trilhas_recomendadas]
        nomes_trilhas = {
            trilha.career_id: trilha.career_name for trilha in trilhas_recomendadas
        }
        if st.session_state["trilha_escolhida"] not in opcoes_trilhas:
            st.session_state["trilha_escolhida"] = opcoes_trilhas[0]

        identificador_escolhido = st.selectbox(
            "Qual trilha deseja usar para montar seu plano?",
            opcoes_trilhas,
            format_func=lambda identificador: nomes_trilhas[identificador],
            key="trilha_escolhida",
        )
        trilha = next(
            trilha
            for trilha in base_conhecimento["career_paths"]
            if trilha["id"] == identificador_escolhido
        )
        competencias_trilha = st.session_state["competencias_por_trilha"].setdefault(
            identificador_escolhido, {}
        )
        minimo = escala_competencias["minimum"]
        maximo = escala_competencias["maximum"]
        st.caption(
            f"Nível-alvo júnior: {escala_competencias['junior_target_level']}. "
            "Habilidades sem avaliação serão consideradas iniciais."
        )
        for habilidade in trilha["junior_skills"]:
            chave_widget = (
                f"widget_competencia_{identificador_escolhido}_{habilidade['id']}"
            )
            if chave_widget not in st.session_state:
                st.session_state[chave_widget] = competencias_trilha.get(
                    habilidade["id"], minimo
                )
            nivel = st.slider(
                habilidade["name"],
                min_value=minimo,
                max_value=maximo,
                step=1,
                key=chave_widget,
            )
            competencias_trilha[habilidade["id"]] = nivel

    st.divider()
    coluna_voltar, coluna_avancar = st.columns(2)
    with coluna_voltar:
        if etapa_atual > 0 and st.button("Voltar", use_container_width=True):
            st.session_state["etapa_atual"] -= 1
            st.rerun()
    with coluna_avancar:
        rotulo_botao = (
            "Gerar diagnóstico"
            if etapa_atual == len(etapas) - 1
            else "Continuar"
        )
        if st.button(rotulo_botao, type="primary", use_container_width=True):
            if etapa_atual == len(etapas) - 1:
                st.session_state["diagnostico_concluido"] = True
            else:
                st.session_state["etapa_atual"] += 1
            st.rerun()