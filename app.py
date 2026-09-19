import streamlit as st
import plotly.express as px
import pandas as pd
from io import BytesIO
from core_analise import MotorAnalise
from dados import processar_metricas_ti

# Bibliotecas para geração de PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Configuração de Layout
st.set_page_config(page_title="Analytics Dashboard Pro", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1 {color: #1E3A8A; font-weight: 700;}
    </style>
""", unsafe_allow_html=True)

st.title("📈 Analytics Dashboard Pro")
st.markdown("Plataforma agnóstica para exploração de dados e geração de indicadores gerenciais.")
st.markdown("---")

# Sidebar - Carga de Arquivos
st.sidebar.header("📁 Fonte de Dados")
arquivo = st.sidebar.file_uploader("Arraste seu relatório corporativo (Excel/CSV):", type=["xlsx", "csv"])

# --- FUNÇÕES DE EXPORTAÇÃO EM MEMÓRIA ---
def gerar_excel_bytes(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False, sheet_name='Dados_Filtrados')
    return output.getvalue()

def gerar_pdf_bytes(dataframe):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#1E3A8A'))
    text_style = ParagraphStyle('TextStyle', parent=styles['Normal'], fontSize=9, leading=12)
    
    story.append(Paragraph("Relatório Gerencial - Dados Filtrados", title_style))
    story.append(Spacer(1, 15))
    
    df_pdf = dataframe.head(30)
    data_tabela = [df_pdf.columns.tolist()]
    for lista_linha in df_pdf.values.tolist():
        linha_texto = [Paragraph(str(item), text_style) for item in lista_linha]
        data_tabela.append(linha_texto)
    
    tabela_pdf = Table(data_tabela, hAlign='LEFT')
    tabela_pdf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tabela_pdf)
    doc.build(story)
    return output.getvalue()

# ==========================================
# 2. SISTEMA DE DADOS INTELIGENTE INICIAL
# ==========================================
if arquivo is not None:
    # Se o usuário subiu um arquivo, ativa o motor analítico dinâmico
    motor = MotorAnalise(arquivo)
    df_bruto = motor.df
    cols_texto = motor.select_colunas_texto()
    cols_num = motor.select_colunas_numericas()
    st.sidebar.success("✅ Arquivo carregado com sucesso!")
else:
    # Correção: Se não houver arquivo, injeta a base de simulação IMEDIATAMENTE na tela
    df_bruto, _, _, _ = processar_metricas_ti()
    cols_texto = ['Tipo', 'Sistema', 'Analista', 'Status_SLA']
    cols_num = ['Tempo_Resolucao_Min', 'Prazo_SLA_Min']
    st.sidebar.info("💡 Exibindo base de simulação padrão. Suba um arquivo para atualizar.")

# ==========================================
# 3. CONFIGURAÇÕES DE VISÃO E FILTROS
# ==========================================
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Configurações de Visão")

eixo_x = st.sidebar.selectbox("Agrupamento Principal (Eixo X):", cols_texto, key="sb_x")
eixo_cor = st.sidebar.selectbox("Sub-agrupamento (Legenda):", ["Nenhum"] + cols_texto, key="sb_cor")

metrica = st.sidebar.radio("Métrica de Análise:", ["Contagem de Registros", "Soma de Valores"])
valor_num = None
if metrica == "Soma de Valores" and cols_num:
    valor_num = st.sidebar.selectbox("Selecione o valor numérico:", cols_num)

st.sidebar.markdown("---")
st.sidebar.header("🎯 Filtros Operacionais")

filtros_ativos = {}
for col in cols_texto[:2]:
    opcoes = df_bruto[col].dropna().unique().tolist()
    selecionados = st.sidebar.multiselect(f"Filtrar por {col}:", opcoes, default=opcoes, key=f"filter_{col}")
    filtros_ativos[col] = Grid_valores = selecionados

# Aplica a filtragem de forma segura
df_filtrado = df_bruto.copy()
for coluna, valores in filtros_ativos.items():
    if valores:
        df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]

# ==========================================
# 4. CARDS DE PERFORMANCE
# ==========================================
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="Volume de Registros Filtrados", value=f"{len(df_filtrado):,}")
with c2:
    if metrica == "Soma de Valores" and valor_num:
        total = df_filtrado[valor_num].sum()
        st.metric(label=f"Métrica Consolidada ({valor_num})", value=f"{total:,.2f}")
    else:
        total_geral = len(df_bruto)
        st.metric(label="Aproveitamento da Base", value=f"{(len(df_filtrado)/total_geral*100):.1f}%" if total_geral > 0 else "0%")
with c3:
    st.metric(label="Colunas Analisadas", value=len(df_bruto.columns))

st.markdown("---")

# ==========================================
# 5. ABAS VISUAIS (GRÁFICOS E DADOS)
# ==========================================
aba_graficos, aba_dados = st.tabs(["📊 Visões Gráficas", "📋 Tabela Gerencial"])

with aba_graficos:
    g1, g2 = st.columns(2)
    cor_param = None if eixo_cor == "Nenhum" else eixo_cor
    
    with g1:
        st.subheader(f"Análise de Distribuição por {eixo_x}")
        if not df_filtrado.empty:
            if metrica == "Soma de Valores" and valor_num:
                df_graf = df_filtrado.groupby([eixo_x] + ([eixo_cor] if cor_param else []))[valor_num].sum().reset_index()
                fig = px.bar(df_graf, x=eixo_x, y=valor_num, color=cor_param, barmode="group", text_auto='.2s', template="plotly_white")
            else:
                df_graf = df_filtrado.groupby([eixo_x] + ([eixo_cor] if cor_param else [])).size().reset_index(name='Quantidade')
                fig = px.bar(df_graf, x=eixo_x, y='Quantidade', color=cor_param, barmode="group", text_auto=True, template="plotly_white")
            
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Ajuste os filtros na barra lateral para exibir os dados.")

    with g2:
        st.subheader(f"Representatividade Percentual por {eixo_x}")
        if not df_filtrado.empty:
            y_param = valor_num if (metrica == "Soma de Valores" and valor_num) else df_filtrado.index
            fig_pizza = px.pie(df_filtrado, names=eixo_x, values=y_param, hole=0.4, template="plotly_white")
            fig_pizza.update_traces(textinfo='percent+label')
            fig_pizza.update_layout(margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_pizza, use_container_width=True)

with aba_dados:
    st.subheader("Visualização Amostral dos Dados")
    
    if not df_filtrado.empty:
        st.markdown("##### 📥 Exportar Base Filtrada")
        btn_col1, btn_col2, _ = st.columns(3)
        with btn_col1:
            st.download_button(
                label="📄 Baixar em Excel",
                data=gerar_excel_bytes(df_filtrado),
                file_name="relatorio_filtrado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        with btn_col2:
            st.download_button(
                label="📕 Baixar em PDF",
                data=gerar_pdf_bytes(df_filtrado),
                file_name="relatorio_filtrado.pdf",
                mime="application/pdf"
            )
        st.markdown("<br>", unsafe_allow_html=True)
        
    st.dataframe(df_filtrado, use_container_width=True)
