from experta import KnowledgeEngine


class ConsultorCarreira(KnowledgeEngine):
    """
    Motor de inferência do Sistema Especialista.
    As regras serão implementadas em rules.py.
    """

    def __init__(self):
        super().__init__()
        self.resultado = None
        self.justificativa = []