# Base de Conhecimento – Consultor Inteligente de Carreiras em TI

## Objetivo

Definir quais características do usuário estão relacionadas a cada uma das dez trilhas de carreira utilizadas pelo Sistema Especialista.

---

## Pontuação, lacunas e recomendações

O fluxo atual carrega a configuração de `regras_carreiras.json`. Os pesos de afinidade são normalizados em uma pontuação de compatibilidade; quando a pessoa informa uma preferência de trabalho, ela é combinada com as afinidades conforme `objective_fit_weight`. A opção "Ainda estou explorando" é neutra.

Cada trilha define habilidades esperadas para o nível júnior e associa lacunas a tecnologias em `roadmap.technology_by_skill`. As tecnologias relacionadas às lacunas são exibidas primeiro. `roadmap.certification_by_skill` permite priorizar certificações ligadas às competências que ainda precisam ser desenvolvidas; se nenhuma lacuna tiver uma certificação específica, são usadas as sugestões gerais da trilha.

O projeto principal do portfólio permanece ligado à trilha, e `portfolio_gap_template` acrescenta as habilidades ainda não atingidas ao foco do projeto. `timeline_guidance` e as horas semanais informadas orientam o ritmo sugerido do plano.

Para ajustar a base sem alterar o motor, atualize os pesos, as habilidades e esses mapas no JSON. O carregamento valida referências a perguntas, trilhas, habilidades, tecnologias, preferências e prazos.

---

## Desenvolvimento Back-end

Características principais:

- Gosta de programação lógica.
- Interesse em APIs.
- Interesse em banco de dados.
- Afinidade com Python ou Java.
- Prefere desenvolver regras de negócio.

---

## Desenvolvimento Front-end & UI/UX

Características principais:

- Gosta de criar interfaces.
- Interesse em experiência do usuário.
- Afinidade com JavaScript.
- Interesse por HTML e CSS.
- Prefere visualizar o resultado das aplicações.

---

## Ciência de Dados e Machine Learning

Características principais:

- Alta afinidade com matemática.
- Interesse em estatística.
- Interesse em Inteligência Artificial.
- Afinidade com Python.
- Gosta de analisar dados.

---

## Engenharia de Dados

Características principais:

- Interesse em bancos de dados.
- Interesse em ETL.
- Interesse em Big Data.
- Gosta de infraestrutura de dados.
- Afinidade com Python.

---

## Cibersegurança

Características principais:

- Interesse em segurança.
- Interesse em redes.
- Afinidade com Linux.
- Interesse em criptografia.
- Gosta de investigar vulnerabilidades.

---

## DevOps & SRE

Características principais:

- Interesse em automação.
- Interesse em servidores.
- Interesse em Docker.
- Interesse em CI/CD.
- Gosta de infraestrutura.

---

## Computação em Nuvem

Características principais:

- Interesse em AWS, Azure ou GCP.
- Interesse em infraestrutura escalável.
- Interesse em virtualização.
- Interesse em arquitetura.
- Gosta de ambientes distribuídos.

---

## Desenvolvimento Mobile

Características principais:

- Interesse em aplicativos móveis.
- Interesse em Android.
- Interesse em iOS.
- Interesse em Flutter ou React Native.
- Gosta de interfaces para dispositivos móveis.

---

## Engenharia de Qualidade (QA)

Características principais:

- Interesse em testes.
- Atenção aos detalhes.
- Interesse em automação de testes.
- Gosta de encontrar falhas.
- Preocupação com qualidade.

---

## Gestão de Produtos

Características principais:

- Interesse em negócios.
- Boa comunicação.
- Interesse em metodologias ágeis.
- Gosta de organizar equipes.
- Interesse em estratégia de produto.