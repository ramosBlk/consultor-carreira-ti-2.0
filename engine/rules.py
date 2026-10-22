from experta import Rule

from engine.inference import ConsultorCarreira
from engine.facts import Usuario
from models.careers import BACKEND
from models.careers import FRONTEND
from models.careers import DATA_SCIENCE
from models.careers import DATA_ENGINEERING
from models.careers import CYBERSECURITY
from models.careers import DEVOPS
from models.careers import CLOUD
from models.careers import MOBILE
from models.careers import QA
from models.careers import PRODUCT


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

    @Rule(
        Usuario(
            matematica="Alta",
            linguagem="Python",
            inteligencia_artificial="Sim"
        )
    )
    def data_science_python(self):
        self.resultado = DATA_SCIENCE
        self.justificativa.append(
            "Alta afinidade com matemática."
        )
        self.justificativa.append(
            "Interesse em Inteligência Artificial."
        )
        self.justificativa.append(
            "Python é amplamente utilizado em Ciência de Dados."
        )

    @Rule(
        Usuario(
            matematica="Alta",
            atividade="Analisar Dados"
        )
    )
    def data_science_analysis(self):
        self.resultado = DATA_SCIENCE
        self.justificativa.append(
            "Interesse em análise de dados."
        )
        self.justificativa.append(
            "Perfil analítico."
        )
        self.justificativa.append(
            "Afinidade com raciocínio matemático."
        )

    @Rule(
        Usuario(
            atividade="Analisar Dados",
            inteligencia_artificial="Sim",
            banco_dados="Sim"
        )
    )
    def data_science_complete(self):
        self.resultado = DATA_SCIENCE
        self.justificativa.append(
            "Interesse em análise de dados."
        )
        self.justificativa.append(
            "Conhecimento em bancos de dados."
        )
        self.justificativa.append(
            "Interesse em Inteligência Artificial."
        )

    @Rule(
        Usuario(
            banco_dados="Sim",
            atividade="Analisar Dados",
            automacao="Sim"
        )
    )
    def data_engineering_pipeline(self):
        self.resultado = DATA_ENGINEERING
        self.justificativa.append("Interesse em bancos de dados.")
        self.justificativa.append("Interesse em automação.")
        self.justificativa.append("Perfil voltado para Engenharia de Dados.")

    @Rule(
        Usuario(
            linguagem="Python",
            banco_dados="Sim",
            entrega="Dados"
        )
    )
    def data_engineering_python(self):
        self.resultado = DATA_ENGINEERING
        self.justificativa.append("Afinidade com Python.")
        self.justificativa.append("Interesse em infraestrutura de dados.")
        self.justificativa.append("Perfil compatível com Engenharia de Dados.")

    @Rule(
        Usuario(
            atividade="Infraestrutura",
            banco_dados="Sim"
        )
    )
    def data_engineering_infra(self):
        self.resultado = DATA_ENGINEERING
        self.justificativa.append("Interesse em infraestrutura.")
        self.justificativa.append("Interesse em bancos de dados.")
        self.justificativa.append("Perfil de Engenharia de Dados.")

    @Rule(
        Usuario(
            atividade="Segurança",
            redes="Sim",
            linguagem="Linux/Redes"
        )
    )
    def cyber_linux(self):
        self.resultado = CYBERSECURITY
        self.justificativa.append("Conhecimento em Linux.")
        self.justificativa.append("Interesse em redes.")
        self.justificativa.append("Perfil voltado para segurança.")

    @Rule(
        Usuario(
            atividade="Segurança",
            entrega="Segurança"
        )
    )
    def cyber_security(self):
        self.resultado = CYBERSECURITY
        self.justificativa.append("Interesse em segurança.")
        self.justificativa.append("Busca proteger sistemas.")
        self.justificativa.append("Perfil compatível com Cibersegurança.")

    @Rule(
        Usuario(
            redes="Sim",
            cloud="Sim"
        )
    )
    def cyber_network(self):
        self.resultado = CYBERSECURITY
        self.justificativa.append("Interesse em redes.")
        self.justificativa.append("Conhecimento em Cloud.")
        self.justificativa.append("Perfil de defesa cibernética.")

    @Rule(
        Usuario(
            automacao="Sim",
            cloud="Sim",
            atividade="Infraestrutura"
        )
    )
    def devops_cloud(self):
        self.resultado = DEVOPS
        self.justificativa.append("Interesse em automação.")
        self.justificativa.append("Interesse em Cloud.")
        self.justificativa.append("Perfil DevOps.")

    @Rule(
        Usuario(
            automacao="Sim",
            redes="Sim"
        )
    )
    def devops_automation(self):
        self.resultado = DEVOPS
        self.justificativa.append("Automação.")
        self.justificativa.append("Conhecimento em redes.")
        self.justificativa.append("Perfil DevOps.")

    @Rule(
        Usuario(
            cloud="Sim",
            atividade="Infraestrutura"
        )
    )
    def cloud_infra(self):
        self.resultado = CLOUD
        self.justificativa.append("Interesse em Cloud.")
        self.justificativa.append("Interesse em infraestrutura.")
        self.justificativa.append("Perfil Cloud.")

    @Rule(
        Usuario(
            cloud="Sim",
            redes="Sim",
            entrega="Infraestrutura"
        )
    )
    def cloud_architecture(self):
        self.resultado = CLOUD
        self.justificativa.append("Arquitetura em nuvem.")
        self.justificativa.append("Conhecimento em redes.")
        self.justificativa.append("Perfil Cloud.")

    @Rule(
        Usuario(
            mobile="Sim",
            atividade="Aplicativos Mobile"
        )
    )
    def mobile_apps(self):
        self.resultado = MOBILE
        self.justificativa.append("Interesse em aplicativos.")
        self.justificativa.append("Perfil Mobile.")
        self.justificativa.append("Gosta de dispositivos móveis.")

    @Rule(
        Usuario(
            linguagem="JavaScript",
            mobile="Sim"
        )
    )
    def mobile_framework(self):
        self.resultado = MOBILE
        self.justificativa.append("Afinidade com JavaScript.")
        self.justificativa.append("Interesse em Mobile.")
        self.justificativa.append("Perfil para Flutter/React Native.")

    @Rule(
        Usuario(
            testes="Sim",
            automacao="Sim"
        )
    )
    def qa_automation(self):
        self.resultado = QA
        self.justificativa.append("Interesse em testes.")
        self.justificativa.append("Automação.")
        self.justificativa.append("Perfil QA.")

    @Rule(
        Usuario(
            testes="Sim",
            entrega="Produto Final"
        )
    )
    def qa_quality(self):
        self.resultado = QA
        self.justificativa.append("Busca qualidade.")
        self.justificativa.append("Interesse em testes.")
        self.justificativa.append("Perfil QA.")

    @Rule(
        Usuario(
            negocios="Sim",
            atividade="Gestão de Produto"
        )
    )
    def product_management(self):
        self.resultado = PRODUCT
        self.justificativa.append("Interesse em gestão.")
        self.justificativa.append("Boa visão de produto.")
        self.justificativa.append("Perfil Product Management.")

    @Rule(
        Usuario(
            negocios="Sim",
            entrega="Produto Final"
        )
    )
    def product_business(self):
        self.resultado = PRODUCT
        self.justificativa.append("Interesse em negócios.")
        self.justificativa.append("Foco em produto.")
        self.justificativa.append("Perfil Product Manager.")