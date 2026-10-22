from experta import Rule

from engine.inference import ConsultorCarreira
from engine.facts import Usuario
from models.careers import BACKEND
from models.careers import FRONTEND


class MotorRegras(ConsultorCarreira):
    """
    Motor de regras do Sistema Especialista.

    Cada regra representa um conhecimento especialista
    utilizado para recomendar uma trilha de carreira.
    """

    @Rule(
        Usuario(
            linguagem="Python",
            atividade="Criar APIs"
        )
    )
    def backend_python(self):
        self.resultado = BACKEND

        self.justificativa.append(
            "Afinidade com Python."
        )

        self.justificativa.append(
            "Interesse em desenvolvimento de APIs."
        )


    @Rule(
        Usuario(
            linguagem="Java",
            atividade="Criar APIs"
        )
    )
    def backend_java(self):
        self.resultado = BACKEND

        self.justificativa.append(
            "Afinidade com Java."
        )

        self.justificativa.append(
            "Interesse em regras de negócio."
        )


    @Rule(
        Usuario(
            atividade="Criar APIs",
            entrega="Infraestrutura"
        )
    )
    def backend_infra(self):
        self.resultado = BACKEND

        self.justificativa.append(
            "Preferência por infraestrutura."
        )

        self.justificativa.append(
            "Interesse em desenvolvimento de APIs."
        )
    @Rule(
    Usuario(
        linguagem="JavaScript",
        atividade="Criar Interfaces"
    )
)
def frontend_javascript(self):
    self.resultado = FRONTEND

    self.justificativa.append(
        "Afinidade com JavaScript."
    )

    self.justificativa.append(
        "Interesse em desenvolvimento de interfaces."
    )

    self.justificativa.append(
        "Perfil voltado para aplicações web."
    )


@Rule(
    Usuario(
        atividade="Criar Interfaces",
        entrega="Produto Final"
    )
)
def frontend_interface(self):
    self.resultado = FRONTEND

    self.justificativa.append(
        "Gosta de criar interfaces para usuários."
    )

    self.justificativa.append(
        "Prefere entregar funcionalidades visíveis ao usuário."
    )

    self.justificativa.append(
        "Perfil compatível com Front-end."
    )


@Rule(
    Usuario(
        atividade="Criar Interfaces",
        mobile="Sim"
    )
)
def frontend_mobile(self):
    self.resultado = FRONTEND

    self.justificativa.append(
        "Interesse por interfaces."
    )

    self.justificativa.append(
        "Interesse em aplicações móveis."
    )

    self.justificativa.append(
        "Perfil compatível com desenvolvimento Front-end."
    )