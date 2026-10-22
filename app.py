import streamlit as st

from engine.rules import MotorRegras
from engine.facts import Usuario
from engine.questions import QUESTIONS

st.set_page_config(
    page_title="Consultor Inteligente de Carreiras em TI",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Consultor Inteligente de Carreiras em TI")

st.write(
    """
    Responda às perguntas abaixo para descobrir qual
    trilha de carreira em Tecnologia da Informação mais
    combina com seu perfil.
    """
)

st.divider()

matematica = st.radio(
    "Qual seu nível de afinidade com Matemática?",
    QUESTIONS["matematica"]
)

programacao_logica = st.radio(
    "Você gosta de programação lógica?",
    QUESTIONS["programacao_logica"]
)

atividade = st.selectbox(
    "Qual atividade você mais gosta?",
    QUESTIONS["atividade"]
)

linguagem = st.selectbox(
    "Qual linguagem possui maior afinidade?",
    QUESTIONS["linguagem"]
)

banco_dados = st.radio(
    "Você gosta de Banco de Dados?",
    QUESTIONS["banco_dados"]
)

automacao = st.radio(
    "Você gosta de Automação?",
    QUESTIONS["automacao"]
)

inteligencia_artificial = st.radio(
    "Você gosta de Inteligência Artificial?",
    QUESTIONS["inteligencia_artificial"]
)

redes = st.radio(
    "Você gosta de Redes?",
    QUESTIONS["redes"]
)

cloud = st.radio(
    "Você gosta de Computação em Nuvem?",
    QUESTIONS["cloud"]
)

testes = st.radio(
    "Você gosta de Testes de Software?",
    QUESTIONS["testes"]
)

mobile = st.radio(
    "Você gosta de Desenvolvimento Mobile?",
    QUESTIONS["mobile"]
)

negocios = st.radio(
    "Você gosta da área de Negócios?",
    QUESTIONS["negocios"]
)

entrega = st.selectbox(
    "Qual tipo de entrega você prefere?",
    QUESTIONS["entrega"]
)

st.divider()

if st.button("🎯 Descobrir minha carreira"):

    motor = MotorRegras()

    motor.reset()

    motor.declare(
        Usuario(
            matematica=matematica,
            programacao_logica=programacao_logica,
            atividade=atividade,
            linguagem=linguagem,
            banco_dados=banco_dados,
            automacao=automacao,
            inteligencia_artificial=inteligencia_artificial,
            redes=redes,
            cloud=cloud,
            testes=testes,
            mobile=mobile,
            negocios=negocios,
            entrega=entrega
        )
    )

    motor.run()

    if motor.resultado:

        st.success("Carreira recomendada:")

        st.header(motor.resultado)

        st.subheader("Justificativa")

        for motivo in motor.justificativa:
            st.write(f"✔ {motivo}")

    else:

        st.warning(
            "Não foi possível identificar uma carreira com as respostas informadas."
        )