# 📈 Analytics Dashboard Pro

O **Analytics Dashboard Pro** é uma plataforma analítica agnóstica e multifuncional desenvolvida em Python. O sistema permite o upload de qualquer relatório corporativo em formato Excel (`.xlsx`) ou CSV (como extrações do Jira, ServiceNow, GLPI ou faturamentos) e gera automaticamente dashboards interativos com inteligência bilíngue para mapeamento de colunas.

---

## 🔗 Acesse a Aplicação em Tempo Real

A aplicação está hospedada na nuvem e pode ser acessada e testada de qualquer dispositivo através do link abaixo:

👉 **[Clique aqui para acessar o Dashboard Online](https://analytics-dashboard-pro.streamlit.app/)**

---

## 🚀 Funcionalidades Chave

- **Mapeamento Agnóstico de Dados:** Identifica de forma automática colunas de texto (categorias) e numéricas (valores), adaptando-se a qualquer modelo de planilha.
- **Filtros Dinâmicos Avançados:** Cria componentes de filtragem na barra lateral com títulos que se adaptam dinamicamente ao nome das colunas selecionadas.
- **Gráficos Interativos (Plotly):** Gráficos de distribuição e percentuais que se atualizam em tempo real conforme as seleções do usuário.
- **Exportação Customizada:** Permite baixar a base de dados refinada pelos filtros em arquivos **Excel** ou **PDF** gerados em tempo real.
- **Arquitetura Modular:** Separação estrita de responsabilidades entre o motor lógico (`core_analise.py`) e a interface visual (`app.py`).

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Streamlit** (Interface Web)
- **Pandas** (Manipulação e Engenharia de Dados)
- **Plotly** (Gráficos Interativos)
- **ReportLab** (Mecanismo de Geração de PDFs)
- **OpenPyXL** (Mecanismo de Escrita de planilhas Excel)

---

## 📦 Como Instalar e Rodar o Projeto

Siga os passos abaixo para clonar o repositório e executar a aplicação na sua máquina local.

### 1. Clonar o Repositório
```bash
git clone https://github.com/ltsilva23/analytics-dashboard-pro
cd NOME_DO_REPOSITORIO
```

### 2. Criar e Ativar Ambiente Virtual (Recomendado)
```bash
# No Windows:
python -m venv venv
venv\Scripts\activate

# No Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação
```bash
streamlit run app.py
```
A aplicação abrirá automaticamente uma aba no seu navegador padrão no endereço `http://localhost:8501`.

---

## 📁 Estrutura do Projeto

```text
├── app.py            # Interface visual e componentes do Streamlit
├── core_analise.py   # Motor lógico de tratamento e filtragem (Pandas)
├── dados.py          # Arquivo auxiliar com dados de simulação padrão
├── .gitignore        # Bloqueio de arquivos locais e confidenciais
├── requirements.txt  # Lista de dependências para instalação na nuvem
└── README.md         # Documentação técnica do projeto
```

---
Desenvolvido como projeto prático focado em Engenharia de Automação e Analytics. ⚡
