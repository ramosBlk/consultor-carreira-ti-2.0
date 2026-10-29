# 🧠 Consultor Inteligente de Carreiras em TI

Sistema de orientação de carreira desenvolvido em Python para auxiliar estudantes e profissionais de Tecnologia da Informação a identificar trilhas compatíveis com seu perfil.

O sistema coleta afinidades em escala Likert, preferência profissional, disponibilidade e conhecimentos atuais. Um motor de pontuação ponderada recomenda as três trilhas mais compatíveis e monta um plano de estudos com lacunas priorizadas para o nível júnior.

---

# 🖥️ Tela de Resultado Esperado 

![Tela do projeto](assets/Tela.png)

![Tela do projeto](assets/Tela2.png)


---
# 🎯 Objetivo

Desenvolver um Sistema Especialista capaz de identificar a trilha de carreira em TI mais compatível com o perfil do usuário utilizando:

- Base de conhecimento externa em JSON;
- Pontuação ponderada e penalidades configuráveis;
- Análise de lacunas por competência;
- Interface Web interativa.

O sistema busca simular o processo de orientação profissional realizado por um especialista humano.

---

# 🚀 Tecnologias Utilizadas

- **Python**  
  Linguagem principal utilizada no desenvolvimento do sistema.

- **Streamlit**  
  Framework utilizado para construção da interface web.

- **Experta**
  Mantida para os testes do motor de regras legado; o fluxo atual da interface usa a pontuação ponderada baseada em `regras_carreiras.json`.

- **Git/GitHub**  
  Controle de versão e armazenamento do projeto.

---

# 📂 Estrutura do Projeto

```
consultor-carreiras-ti/
│
├── app.py                     # Interface Web utilizando Streamlit
├── requirements.txt            # Dependências do projeto
├── regras_carreiras.json       # Perguntas, pesos, trilhas, gaps e recomendações
├── decision_matrix.md          # Matriz histórica das regras legadas
├── knowledge_base.md           # Documentação da base de conhecimento
├── README.md                   # Documentação do projeto
│
├── engine/                     # Núcleo do sistema especialista
│   │
│   ├── __init__.py             # Compatibilidade das dependências do motor
│   ├── engine.py               # Carregamento JSON e ranking ponderado
│   ├── roadmap.py              # Análise de gaps e plano de estudos
│   ├── facts.py                # Definição dos fatos do usuário
│   ├── inference.py            # Motor de inferência legado utilizando Experta
│   ├── questions.py            # Perguntas da entrevista
│   └── rules.py                # Regras especialistas legadas
│
├── models/
│   └── careers.py              # Definição das trilhas de carreira
│
└── tests/
    ├── test_weighted_engine.py # Testes do ranking ponderado
    ├── test_roteiro.py         # Testes de lacunas e roadmap
    ├── test_casos_limite.py    # Testes de perfis ambíguos e limites
    └── test_rules.py           # Testes do motor legado
```

---

# 🧠 Funcionamento do Sistema

O fluxo atual utiliza uma base de conhecimento desacoplada e um motor de pontuação ponderada.

O fluxo de funcionamento ocorre da seguinte forma:

```
Usuário
   |
   ↓
Wizard de três etapas
   |
   ↓
Afinidades de 1 a 5 + objetivos
   |
   ↓
Ranking ponderado das dez trilhas
   |
   ↓
Top 3 + trilha escolhida
   |
   ↓
Lacunas para nível júnior + roadmap
```

Os pesos das perguntas, penalidades, habilidades júnior, tecnologias, certificações e projetos ficam em `regras_carreiras.json`, não no código do motor. A preferência de trabalho participa do ranking com o peso configurado em `objective_fit_weight`; a opção exploratória não altera o resultado baseado em afinidades.

Para o roadmap, as tecnologias associadas às habilidades com gaps são priorizadas. O prazo profissional e as horas semanais informadas também geram uma orientação de ritmo; certificações e projetos são sugeridos conforme a trilha selecionada.

---

# 🎯 Trilhas de Carreira Disponíveis

O sistema pode recomendar uma das 10 trilhas:

## 1. Desenvolvimento Back-end

Foco em:

- Construção de APIs;
- Regras de negócio;
- Desenvolvimento de servidores;
- Banco de dados.

---

## 2. Desenvolvimento Front-end & UI/UX

Foco em:

- Interfaces web;
- Experiência do usuário;
- Design de aplicações;
- Frameworks modernos.

---

## 3. Ciência de Dados e Machine Learning

Foco em:

- Inteligência Artificial;
- Estatística;
- Modelos preditivos;
- Análise de dados.

---

## 4. Engenharia de Dados

Foco em:

- Arquitetura de dados;
- Pipelines ETL/ELT;
- Processamento de grandes volumes de dados;
- Data Lakes.

---

## 5. Cibersegurança

Foco em:

- Segurança digital;
- Redes;
- Vulnerabilidades;
- Proteção de sistemas.

---

## 6. DevOps & SRE

Foco em:

- Automação;
- Integração contínua (CI/CD);
- Contêineres;
- Infraestrutura.

---

## 7. Computação em Nuvem

Foco em:

- Arquitetura Cloud;
- AWS, Azure e GCP;
- Escalabilidade;
- Gestão de infraestrutura.

---

## 8. Desenvolvimento Mobile

Foco em:

- Aplicativos móveis;
- Desenvolvimento Android/iOS;
- Flutter;
- React Native.

---

## 9. Engenharia de Qualidade e Testes (QA)

Foco em:

- Testes automatizados;
- Qualidade de software;
- Confiabilidade;
- Processos de validação.

---

## 10. Gestão de Produtos

Foco em:

- Estratégia de produto;
- Metodologias ágeis;
- Comunicação entre negócio e desenvolvimento;
- Priorização de funcionalidades.

---

# ⚙️ Instalação

## 1. Clonar o repositório

```bash
git clone https://github.com/ramosBlk/consultor-carreiras-ti.git
```

Acesse a pasta:

```bash
cd consultor-carreiras-ti
```

---

## 2. Criar ambiente virtual

```bash
python -m venv .venv
```

Ativar ambiente virtual:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# ▶️ Executando o Sistema

Com o ambiente virtual ativado:

```bash
streamlit run app.py
```

O sistema será aberto automaticamente no navegador:

```
http://localhost:8501
```

---

# 📋 Motor de Inferência

O sistema utiliza regras do tipo:

```
SE condição
ENTÃO recomendação
```

Exemplo:

```
SE usuário possui afinidade com Python
E gosta de criar APIs

ENTÃO recomendar Desenvolvimento Back-end
```

Cada regra possui uma justificativa associada, permitindo transparência na decisão.

---

# 🧪 Validação com Personas

Para executar os testes automatizados com as dependências instaladas:

```bash
python -m unittest discover -s tests
```

Os testes cobrem perfis representativos das dez trilhas, um perfil sem
recomendação e a consistência das opções da entrevista.

---

O sistema será validado utilizando diferentes perfis de usuários.

## Persona 1 - Perfil Analítico

Características:

- Alta afinidade matemática;
- Interesse em dados;
- Interesse em inteligência artificial.

Resultado esperado:

```
Ciência de Dados e Machine Learning
```

---

## Persona 2 - Perfil Desenvolvimento

Características:

- Interesse em programação;
- Gosta de lógica;
- Interesse em APIs.

Resultado esperado:

```
Desenvolvimento Back-end
```

---

## Persona 3 - Perfil Infraestrutura

Características:

- Interesse em servidores;
- Redes;
- Cloud;
- Automação.

Resultado esperado:

```
DevOps & SRE
ou
Computação em Nuvem
```

---

## Persona 4 - Perfil Negócios

Características:

- Interesse em produto;
- Comunicação;
- Estratégia.

Resultado esperado:

```
Gestão de Produtos
```

---

# 📚 Engenharia de Conhecimento

O projeto possui documentos auxiliares:

## decision_matrix.md

Contém a matriz de decisão utilizada para estruturar como as respostas do usuário ativam as regras do sistema.

## knowledge_base.md

Contém a organização do conhecimento especialista utilizado pelo motor de inferência.

---

# 👨‍💻 Autor

**Pedro Henrique Ramos de Carvalho**

Projeto acadêmico desenvolvido para a disciplina de Inteligência Artificial.

**Centro Universitário Presidente Antônio Carlos - UNIPAC Barbacena**

# 🤖 Uso de Inteligência Artificial como Apoio no Desenvolvimento

Durante o desenvolvimento deste projeto, foi utilizada a ferramenta **ChatGPT** como recurso de apoio para auxiliar na organização das ideias, estruturação do projeto.

A utilização da inteligência artificial teve como objetivo auxiliar o processo de aprendizagem e desenvolvimento, enquanto todas as decisões de implementação, organização do código, criação das regras do sistema especialista e validação do funcionamento foram realizadas durante a construção do projeto.

A ferramenta foi utilizada como um suporte semelhante a uma consulta técnica, contribuindo para a evolução do projeto e para o entendimento das tecnologias utilizadas.
