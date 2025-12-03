import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Dashboard Saneamento",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# IMPORTAÇÃO DOS DADOS DOS ARQUIVOS CSV
# ============================================

# Caminho base dos dados
DADOS_PATH = os.path.join(os.path.dirname(__file__), 'dados')

# Carregando os bancos de dados
@st.cache_data
def carregar_dados():
    """Carrega todos os dados dos arquivos CSV"""
    
    # Dados de Saúde - DATASUS 2023
    df_saude = pd.read_csv(os.path.join(DADOS_PATH, 'saude_datasus_2023.csv'))
    
    # Dados de Renda - IBGE 2023
    df_renda = pd.read_csv(os.path.join(DADOS_PATH, 'renda_ibge_2023.csv'))
    
    # Dados de Educação - IBGE/INEP 2023
    df_educacao = pd.read_csv(os.path.join(DADOS_PATH, 'educacao_ibge_inep_2023.csv'))
    
    # Dados de Cobertura - SINISA 2023
    df_cobertura = pd.read_csv(os.path.join(DADOS_PATH, 'cobertura_sinisa_2023.csv'))
    
    return df_saude, df_renda, df_educacao, df_cobertura

# Carregar dados
df_saude, df_renda, df_educacao, df_cobertura = carregar_dados()

# ============================================
# PROCESSAMENTO DOS DADOS IMPORTADOS
# ============================================

# Extraindo valores dos DataFrames para o dicionário DADOS_DF
DADOS_DF = {
    # Saúde (DATASUS 2023) - agregados do CSV
    'internacoes_total': df_saude['internacoes'].sum(),
    'custo_internacoes': df_saude['custo_total'].sum(),
    'obitos': df_saude['obitos'].sum(),
    'populacao': df_cobertura[df_cobertura['indicador'] == 'populacao_total']['valor'].values[0],
    
    # Renda (IBGE 2023) - do CSV
    'renda_com_saneamento': df_renda[df_renda['categoria'] == 'com_saneamento']['renda_media_mensal'].values[0],
    'renda_sem_saneamento': df_renda[df_renda['categoria'] == 'sem_saneamento']['renda_media_mensal'].values[0],
    
    # Educação (IBGE/INEP 2023) - do CSV
    'escolaridade_com': df_educacao[df_educacao['indicador'] == 'escolaridade']['com_saneamento'].values[0],
    'escolaridade_sem': df_educacao[df_educacao['indicador'] == 'escolaridade']['sem_saneamento'].values[0],
    'enem_com_banheiro': df_educacao[df_educacao['indicador'] == 'nota_enem']['com_saneamento'].values[0],
    'enem_sem_banheiro': df_educacao[df_educacao['indicador'] == 'nota_enem']['sem_saneamento'].values[0],
    
    # Cobertura (SINISA 2023) - do CSV
    'pop_sem_agua': df_cobertura[df_cobertura['indicador'] == 'sem_agua_tratada']['valor'].values[0],
    'pop_sem_esgoto': df_cobertura[df_cobertura['indicador'] == 'sem_coleta_esgoto']['valor'].values[0],
    'perc_sem_agua': df_cobertura[df_cobertura['indicador'] == 'sem_agua_tratada']['percentual'].values[0],
    'perc_sem_esgoto': df_cobertura[df_cobertura['indicador'] == 'sem_coleta_esgoto']['percentual'].values[0],
}

# Cálculos derivados
DADOS_DF['custo_medio_internacao'] = DADOS_DF['custo_internacoes'] / DADOS_DF['internacoes_total']
DADOS_DF['diferenca_renda'] = DADOS_DF['renda_com_saneamento'] - DADOS_DF['renda_sem_saneamento']
DADOS_DF['diferenca_escolaridade'] = DADOS_DF['escolaridade_com'] - DADOS_DF['escolaridade_sem']
DADOS_DF['diferenca_enem'] = DADOS_DF['enem_com_banheiro'] - DADOS_DF['enem_sem_banheiro']

# ============================================
# CORES DO TEMA ESCURO (Estilo Dashboard)
# ============================================
CORES = {
    'bg_escuro': '#1a1a2e',
    'bg_card': '#16213e',
    'grid': '#2d3a4f',
    'texto': '#e0e0e0',
    'azul': '#4dabf7',
    'azul_claro': '#74c0fc',
    'laranja': '#ff6b35',
    'laranja_claro': '#ff8c5a',
    'verde': '#51cf66',
    'verde_claro': '#8ce99a',
    'vermelho': '#ff6b6b',
    'vermelho_claro': '#ffa8a8',
    'rosa': '#f06595',
    'rosa_claro': '#faa2c1',
    'amarelo': '#ffd43b',
    'roxo': '#9775fa',
    'cyan': '#22b8cf',
}

# ============================================
# CSS CUSTOMIZADO - TEMA ÁGUA
# ============================================
st.markdown("""
<style>
    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tema principal - Gradiente água */
    .stApp {
        background: linear-gradient(135deg, #caf0f8 0%, #90e0ef 25%, #00b4d8 50%, #0077b6 75%, #023e8a 100%);
        background-attachment: fixed;
    }
    
    /* Container principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Título principal com gradiente */
    .titulo-principal {
        background: linear-gradient(90deg, #023e8a, #0077b6, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Subtítulo */
    .subtitulo {
        color: #023e8a;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Cards de impacto no banner */
    .banner-impacto {
        background: linear-gradient(135deg, #023e8a 0%, #0077b6 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    .banner-numero {
        color: #ffd60a;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
    }
    
    .banner-texto {
        color: #caf0f8;
        font-size: 1rem;
        text-align: center;
    }
    
    /* Seções */
    .secao-titulo {
        color: #023e8a;
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #0077b6;
    }
    
    /* Cards de métricas coloridos */
    .card-metrica {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .card-metrica:hover {
        transform: translateY(-5px);
    }
    
    .card-saude {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
    }
    
    .card-renda {
        background: linear-gradient(135deg, #f9ca24 0%, #f0932b 100%);
        color: #1a1a2e;
    }
    
    .card-educacao {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        color: white;
    }
    
    .card-numero {
        font-size: 2rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .card-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Box informativo - CORRIGIDO para texto legível */
    .box-info {
        background: rgba(255, 255, 255, 0.95);
        border-left: 5px solid #0077b6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1a1a2e;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .box-info strong, .box-info b {
        color: #023e8a;
    }
    
    .box-info ul, .box-info ol {
        color: #333;
    }
    
    .box-alerta {
        background: linear-gradient(135deg, #ffe066 0%, #ffd60a 100%);
        border-left: 5px solid #f0932b;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #1a1a2e;
    }
    
    /* Ciclos */
    .ciclo-vicioso {
        background: linear-gradient(135deg, #ff6b6b 0%, #c0392b 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
    }
    
    .ciclo-virtuoso {
        background: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
    }
    
    .ciclo-item {
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        font-size: 0.95rem;
    }
    
    /* Conclusões - CORRIGIDO para texto legível */
    .card-conclusao {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1a1a2e;
    }
    
    .card-conclusao h4 {
        color: #023e8a;
        margin-bottom: 0.5rem;
    }
    
    .card-conclusao p {
        color: #333;
    }
    
    .borda-saude { border-left: 5px solid #ff6b6b; }
    .borda-renda { border-left: 5px solid #f9ca24; }
    .borda-educacao { border-left: 5px solid #6c5ce7; }
    
    /* Rodapé - CORRIGIDO para texto legível */
    .rodape {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        color: #1a1a2e;
    }
    
    .rodape h4 {
        color: #023e8a;
    }
    
    .rodape p {
        color: #333;
    }
    
    .rodape a {
        color: #0077b6;
        text-decoration: none;
        font-weight: bold;
    }
    
    .rodape a:hover {
        color: #023e8a;
        text-decoration: underline;
    }
    
    .creditos {
        background: linear-gradient(135deg, #023e8a 0%, #0077b6 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    
    /* Métricas do Streamlit */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #023e8a;
    }
    
    /* Tabs customizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #caf0f8;
        border-radius: 10px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0077b6;
        color: white;
    }
    
    /* Texto explicativo - CORRIGIDO */
    .texto-explicativo {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
        color: #333;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÃO PARA CRIAR LAYOUT DE GRÁFICO ESTILO ESCURO
# ============================================
def get_dark_layout(title="", height=450, showlegend=True):
    """Retorna layout padrão estilo escuro para gráficos"""
    return dict(
        title=dict(
            text=title,
            font=dict(size=20, color=CORES['texto'], family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor=CORES['bg_escuro'],
        plot_bgcolor=CORES['bg_escuro'],
        font=dict(color=CORES['texto'], family='Arial'),
        height=height,
        showlegend=showlegend,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=12, color=CORES['texto']),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(t=80, b=80, l=60, r=60),
        xaxis=dict(
            gridcolor=CORES['grid'],
            linecolor=CORES['grid'],
            tickfont=dict(color=CORES['texto']),
            title_font=dict(color=CORES['texto'])
        ),
        yaxis=dict(
            gridcolor=CORES['grid'],
            linecolor=CORES['grid'],
            tickfont=dict(color=CORES['texto']),
            title_font=dict(color=CORES['texto'])
        ),
        hoverlabel=dict(
            bgcolor=CORES['bg_card'],
            font_size=14,
            font_family='Arial'
        )
    )

# ============================================
# 1. HEADER E INTRODUÇÃO
# ============================================
st.markdown('<h1 class="titulo-principal">💧 A Disparidade Silenciosa</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">Como o Saneamento Básico Modela a Saúde, Renda e Educação no Distrito Federal</p>', unsafe_allow_html=True)

# Banner de impacto
st.markdown(f"""
<div class="banner-impacto">
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div style="text-align: center; padding: 1rem;">
            <div class="banner-numero">{DADOS_DF['pop_sem_esgoto']:,}</div>
            <div class="banner-texto">pessoas sem coleta de esgoto</div>
        </div>
        <div style="text-align: center; padding: 1rem;">
            <div class="banner-numero">{DADOS_DF['pop_sem_agua']:,}</div>
            <div class="banner-texto">pessoas sem água tratada</div>
        </div>
    </div>
</div>
""".replace(",", "."), unsafe_allow_html=True)

# ============================================
# 2. PANORAMA GERAL
# ============================================
st.markdown("---")
st.markdown('<h2 class="secao-titulo">📊 Panorama Geral do Distrito Federal</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👥 População Total",
        value=f"{DADOS_DF['populacao']:,}".replace(",", ".")
    )

with col2:
    st.metric(
        label="🚰 Sem Água Tratada",
        value=f"{DADOS_DF['pop_sem_agua']:,}".replace(",", "."),
        delta=f"-{DADOS_DF['perc_sem_agua']}%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="🚽 Sem Coleta de Esgoto",
        value=f"{DADOS_DF['pop_sem_esgoto']:,}".replace(",", "."),
        delta=f"-{DADOS_DF['perc_sem_esgoto']}%",
        delta_color="inverse"
    )

with col4:
    st.metric(
        label="🏥 Internações por Doenças Hídricas",
        value=f"{DADOS_DF['internacoes_total']:,}".replace(",", ".")
    )

# ============================================
# 3. SEÇÃO SAÚDE
# ============================================
st.markdown("---")
st.markdown('<h2 class="secao-titulo">🏥 Impacto na Saúde: O Custo das Doenças Evitáveis</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="texto-explicativo">
A falta de saneamento básico está diretamente ligada ao aumento de doenças de veiculação hídrica, 
como diarreias, hepatite A, cólera e outras infecções gastrointestinais. Em 2023, o Distrito Federal 
registrou milhares de internações que poderiam ter sido evitadas com investimentos adequados em 
infraestrutura de água e esgoto.
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card-metrica card-saude">
        <div class="card-label">💰 Custo Total das Internações</div>
        <div class="card-numero">R$ {DADOS_DF['custo_internacoes']:,.2f}</div>
        <div class="card-label">gastos pelo SUS em 2023</div>
    </div>
    """.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card-metrica card-saude">
        <div class="card-label">📋 Custo Médio por Internação</div>
        <div class="card-numero">R$ {DADOS_DF['custo_medio_internacao']:,.2f}</div>
        <div class="card-label">por paciente</div>
    </div>
    """.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card-metrica card-saude">
        <div class="card-label">⚠️ Óbitos Registrados</div>
        <div class="card-numero">{DADOS_DF['obitos']}</div>
        <div class="card-label">mortes evitáveis</div>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de Área - Internações ao longo do ano (Dados do CSV)
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
# Dados reais importados do CSV de saúde
internacoes_mensais = df_saude['internacoes'].tolist()
media_movel = pd.Series(internacoes_mensais).rolling(window=3, min_periods=1).mean().tolist()

fig_saude = go.Figure()

# Área preenchida para internações
fig_saude.add_trace(go.Scatter(
    x=meses,
    y=internacoes_mensais,
    fill='tozeroy',
    fillcolor='rgba(77, 171, 247, 0.3)',
    line=dict(color=CORES['azul'], width=1),
    mode='lines',
    name='Internações Mensais',
    hovertemplate='<b>%{x}</b><br>Internações: %{y}<extra></extra>'
))

# Linha de média móvel
fig_saude.add_trace(go.Scatter(
    x=meses,
    y=media_movel,
    line=dict(color=CORES['laranja'], width=3),
    mode='lines',
    name='Média Móvel (3 meses)',
    hovertemplate='<b>%{x}</b><br>Média: %{y:.0f}<extra></extra>'
))

# Marcador de pico
pico_idx = internacoes_mensais.index(max(internacoes_mensais))
fig_saude.add_trace(go.Scatter(
    x=[meses[pico_idx]],
    y=[max(internacoes_mensais)],
    mode='markers+text',
    marker=dict(size=15, color=CORES['amarelo'], symbol='circle', line=dict(color='white', width=2)),
    text=['Pico'],
    textposition='top center',
    textfont=dict(color=CORES['amarelo'], size=12),
    name='Pico de Internações',
    showlegend=False
))

fig_saude.update_layout(**get_dark_layout(
    title='📈 Internações por Doenças Hídricas ao Longo de 2023',
    height=400
))
fig_saude.update_yaxes(title_text='Número de Internações')
fig_saude.update_xaxes(title_text='Mês')

st.plotly_chart(fig_saude, use_container_width=True)

# Gráfico de Barras com área - Custos (Dados do CSV)
fig_custos = go.Figure()

custos_mensais = df_saude['custo_total'].tolist()

fig_custos.add_trace(go.Bar(
    x=meses,
    y=custos_mensais,
    marker=dict(
        color=custos_mensais,
        colorscale=[[0, CORES['azul']], [0.5, CORES['rosa']], [1, CORES['vermelho']]],
        line=dict(color=CORES['rosa'], width=1)
    ),
    name='Custo Mensal',
    hovertemplate='<b>%{x}</b><br>Custo: R$ %{y:,.2f}<extra></extra>'
))

# Linha de referência
fig_custos.add_hline(
    y=DADOS_DF['custo_internacoes']/12,
    line_dash="dash",
    line_color=CORES['amarelo'],
    annotation_text=f"Média Mensal: R$ {DADOS_DF['custo_internacoes']/12:,.0f}".replace(",", "."),
    annotation_position="right",
    annotation_font=dict(color=CORES['amarelo'], size=12)
)

fig_custos.update_layout(**get_dark_layout(
    title='💰 Custo Mensal das Internações (R$)',
    height=400,
    showlegend=False
))
fig_custos.update_yaxes(title_text='Custo (R$)', tickprefix='R$ ')

st.plotly_chart(fig_custos, use_container_width=True)

st.markdown("""
<div class="box-info">
    <strong>💡 Custos Indiretos:</strong> Além dos custos diretos com internações, a falta de saneamento gera 
    custos indiretos significativos: perda de produtividade, faltas ao trabalho e escola, gastos com medicamentos 
    e tratamentos ambulatoriais, e impacto psicológico nas famílias afetadas.
</div>
""", unsafe_allow_html=True)

# ============================================
# 4. SEÇÃO RENDA
# ============================================
st.markdown("---")
st.markdown('<h2 class="secao-titulo">💰 Impacto na Renda: A Desigualdade Econômica</h2>', unsafe_allow_html=True)

st.markdown(f"""
<div class="texto-explicativo">
A diferença de renda entre domicílios com e sem saneamento adequado é de 
<b>R$ {DADOS_DF['diferenca_renda']:,.2f}</b> por mês. Isso representa muito mais do que um número — 
é a materialização de um ciclo de desigualdade que se perpetua por gerações.
</div>
""".replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

# Gráfico de Área - Evolução da Renda Acumulada
anos = list(range(0, 21))
renda_com_acum = [DADOS_DF['renda_com_saneamento'] * 12 * ano for ano in anos]
renda_sem_acum = [DADOS_DF['renda_sem_saneamento'] * 12 * ano for ano in anos]
diferenca_acum = [c - s for c, s in zip(renda_com_acum, renda_sem_acum)]

fig_renda = go.Figure()

# Área para renda com saneamento
fig_renda.add_trace(go.Scatter(
    x=anos,
    y=renda_com_acum,
    fill='tozeroy',
    fillcolor='rgba(81, 207, 102, 0.3)',
    line=dict(color=CORES['verde'], width=3),
    mode='lines',
    name='Com Saneamento',
    hovertemplate='<b>Ano %{x}</b><br>Renda Acumulada: R$ %{y:,.0f}<extra></extra>'
))

# Área para renda sem saneamento
fig_renda.add_trace(go.Scatter(
    x=anos,
    y=renda_sem_acum,
    fill='tozeroy',
    fillcolor='rgba(255, 107, 53, 0.3)',
    line=dict(color=CORES['laranja'], width=3),
    mode='lines',
    name='Sem Saneamento',
    hovertemplate='<b>Ano %{x}</b><br>Renda Acumulada: R$ %{y:,.0f}<extra></extra>'
))

# Linha vertical marcando 10 anos
fig_renda.add_vline(
    x=10,
    line_dash="dash",
    line_color=CORES['amarelo'],
    annotation_text="10 Anos",
    annotation_position="top",
    annotation_font=dict(color=CORES['amarelo'], size=12)
)

# Anotação da diferença em 20 anos
fig_renda.add_annotation(
    x=20, y=diferenca_acum[-1]/2 + renda_sem_acum[-1],
    text=f"<b>Diferença em 20 anos:<br>R$ {diferenca_acum[-1]:,.0f}</b>".replace(",", "."),
    showarrow=True,
    arrowhead=2,
    arrowcolor=CORES['amarelo'],
    font=dict(size=14, color=CORES['amarelo']),
    bgcolor=CORES['bg_card'],
    bordercolor=CORES['amarelo'],
    borderwidth=2,
    borderpad=8,
    ax=-80,
    ay=-40
)

fig_renda.update_layout(**get_dark_layout(
    title='📈 Evolução da Renda Acumulada ao Longo dos Anos',
    height=450
))
fig_renda.update_xaxes(title_text='Anos', dtick=5)
fig_renda.update_yaxes(title_text='Renda Acumulada (R$)', tickprefix='R$ ')

st.plotly_chart(fig_renda, use_container_width=True)

# Gráfico de barras comparativo
fig_comp_renda = go.Figure()

categorias_renda = ['Renda Mensal', 'Renda Anual', 'Renda em 5 Anos', 'Renda em 10 Anos']
valores_com = [
    DADOS_DF['renda_com_saneamento'],
    DADOS_DF['renda_com_saneamento'] * 12,
    DADOS_DF['renda_com_saneamento'] * 12 * 5,
    DADOS_DF['renda_com_saneamento'] * 12 * 10
]
valores_sem = [
    DADOS_DF['renda_sem_saneamento'],
    DADOS_DF['renda_sem_saneamento'] * 12,
    DADOS_DF['renda_sem_saneamento'] * 12 * 5,
    DADOS_DF['renda_sem_saneamento'] * 12 * 10
]

fig_comp_renda.add_trace(go.Bar(
    name='Com Saneamento',
    x=categorias_renda,
    y=valores_com,
    marker=dict(color=CORES['verde'], line=dict(color=CORES['verde_claro'], width=2)),
    text=[f"R$ {v:,.0f}".replace(",", ".") for v in valores_com],
    textposition='outside',
    textfont=dict(color=CORES['verde'], size=11)
))

fig_comp_renda.add_trace(go.Bar(
    name='Sem Saneamento',
    x=categorias_renda,
    y=valores_sem,
    marker=dict(color=CORES['vermelho'], line=dict(color=CORES['vermelho_claro'], width=2)),
    text=[f"R$ {v:,.0f}".replace(",", ".") for v in valores_sem],
    textposition='outside',
    textfont=dict(color=CORES['vermelho'], size=11)
))

fig_comp_renda.update_layout(**get_dark_layout(
    title='💵 Comparativo de Renda: Com vs Sem Saneamento',
    height=450
))
fig_comp_renda.update_layout(barmode='group')
fig_comp_renda.update_yaxes(title_text='Valor (R$)', tickprefix='R$ ')

st.plotly_chart(fig_comp_renda, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="box-info">
        <strong>📈 Impacto Acumulado:</strong>
        <ul>
            <li><b>1 ano:</b> R$ 13.354,80 de diferença</li>
            <li><b>5 anos:</b> R$ 66.774,00 de diferença</li>
            <li><b>10 anos:</b> R$ 133.548,00 de diferença</li>
            <li><b>20 anos:</b> R$ 267.096,00 de diferença</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="box-info">
        <strong>🔄 Ciclo da Pobreza:</strong>
        <ol>
            <li>Falta de saneamento → mais doenças</li>
            <li>Mais doenças → mais faltas ao trabalho</li>
            <li>Mais faltas → menor produtividade</li>
            <li>Menor produtividade → menor renda</li>
            <li>Menor renda → continua sem saneamento</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 5. SEÇÃO EDUCAÇÃO
# ============================================
st.markdown("---")
st.markdown('<h2 class="secao-titulo">🎓 Impacto na Educação: O Futuro Comprometido</h2>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 Anos de Escolaridade", "📝 Desempenho no ENEM"])

with tab1:
    st.markdown(f"""
    <div class="texto-explicativo">
    A diferença de <b>{DADOS_DF['diferenca_escolaridade']:.2f} anos</b> de escolaridade entre pessoas com e sem 
    acesso a saneamento representa quase <b>2 anos a menos de estudo</b> - o equivalente a não completar 
    o ensino fundamental.
    </div>
    """.replace(".", ","), unsafe_allow_html=True)
    
    # Gráfico de área - Progressão escolar simulada
    idades = list(range(6, 26))
    escolaridade_com = [min(max(0, (idade - 6) * 0.95), DADOS_DF['escolaridade_com']) for idade in idades]
    escolaridade_sem = [min(max(0, (idade - 6) * 0.78), DADOS_DF['escolaridade_sem']) for idade in idades]
    
    fig_escol = go.Figure()
    
    # Área com saneamento
    fig_escol.add_trace(go.Scatter(
        x=idades,
        y=escolaridade_com,
        fill='tozeroy',
        fillcolor='rgba(77, 171, 247, 0.4)',
        line=dict(color=CORES['azul'], width=3),
        mode='lines',
        name='Com Saneamento',
        hovertemplate='<b>Idade: %{x} anos</b><br>Escolaridade: %{y:.1f} anos<extra></extra>'
    ))
    
    # Área sem saneamento
    fig_escol.add_trace(go.Scatter(
        x=idades,
        y=escolaridade_sem,
        fill='tozeroy',
        fillcolor='rgba(240, 101, 149, 0.4)',
        line=dict(color=CORES['rosa'], width=3),
        mode='lines',
        name='Sem Saneamento',
        hovertemplate='<b>Idade: %{x} anos</b><br>Escolaridade: %{y:.1f} anos<extra></extra>'
    ))
    
    # Linha de referência - Ensino Médio completo
    fig_escol.add_hline(
        y=12,
        line_dash="dash",
        line_color=CORES['amarelo'],
        annotation_text="Ensino Médio Completo",
        annotation_position="right",
        annotation_font=dict(color=CORES['amarelo'], size=11)
    )
    
    # Marcador do GAP
    fig_escol.add_annotation(
        x=25, y=(DADOS_DF['escolaridade_com'] + DADOS_DF['escolaridade_sem'])/2,
        text=f"<b>GAP: {DADOS_DF['diferenca_escolaridade']:.2f} anos</b>".replace(".", ","),
        showarrow=True,
        arrowhead=2,
        arrowcolor=CORES['amarelo'],
        font=dict(size=14, color=CORES['texto']),
        bgcolor=CORES['bg_card'],
        bordercolor=CORES['amarelo'],
        borderwidth=2,
        borderpad=8,
        ax=-60,
        ay=0
    )
    
    fig_escol.update_layout(**get_dark_layout(
        title='📚 Progressão da Escolaridade por Idade',
        height=450
    ))
    fig_escol.update_xaxes(title_text='Idade (anos)', dtick=2)
    fig_escol.update_yaxes(title_text='Anos de Estudo', dtick=2)
    
    st.plotly_chart(fig_escol, use_container_width=True)
    
    st.markdown("""
    <div class="box-info">
        <strong>📖 O que isso significa:</strong><br>
        Quase 2 anos a menos de estudo impactam diretamente nas oportunidades de emprego, 
        capacidade de compreensão de direitos, acesso a informações de saúde e participação 
        cidadã. É um ciclo que se perpetua por gerações.
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown(f"""
    <div class="texto-explicativo">
    A diferença de <b>{DADOS_DF['diferenca_enem']:.2f} pontos</b> no ENEM entre estudantes com e sem 
    banheiro adequado pode significar a diferença entre entrar ou não em uma universidade pública.
    </div>
    """.replace(".", ","), unsafe_allow_html=True)
    
    # Gráfico de barras estilo lollipop com fundo escuro
    fig_enem = go.Figure()
    
    categorias_enem = ['Com Banheiro Adequado', 'Sem Banheiro Adequado']
    valores_enem = [DADOS_DF['enem_com_banheiro'], DADOS_DF['enem_sem_banheiro']]
    cores_enem = [CORES['cyan'], CORES['rosa']]
    
    # Barras
    for i, (cat, val, cor) in enumerate(zip(categorias_enem, valores_enem, cores_enem)):
        # Linha vertical (stem)
        fig_enem.add_trace(go.Scatter(
            x=[cat, cat],
            y=[0, val],
            mode='lines',
            line=dict(color=cor, width=20),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Círculo no topo
        fig_enem.add_trace(go.Scatter(
            x=[cat],
            y=[val],
            mode='markers+text',
            marker=dict(size=50, color=cor, line=dict(color='white', width=3)),
            text=[f"{val:.1f}".replace(".", ",")],
            textposition='middle center',
            textfont=dict(size=14, color='white', family='Arial Black'),
            name=cat,
            hovertemplate=f'<b>{cat}</b><br>Nota: {val:.2f} pontos<extra></extra>'
        ))
    
    # Linha de referência - média nacional
    fig_enem.add_hline(
        y=500,
        line_dash="dash",
        line_color=CORES['amarelo'],
        line_width=3,
        annotation_text="📌 Média Nacional (500 pts)",
        annotation_position="right",
        annotation_font=dict(color=CORES['amarelo'], size=13, family='Arial Black')
    )
    
    # Anotação da diferença
    fig_enem.add_annotation(
        x=0.5, y=420,
        xref='paper',
        text=f"<b>Diferença: {DADOS_DF['diferenca_enem']:.2f} pontos</b>".replace(".", ","),
        showarrow=False,
        font=dict(size=16, color=CORES['texto']),
        bgcolor=CORES['vermelho'],
        bordercolor=CORES['vermelho_claro'],
        borderwidth=2,
        borderpad=10
    )
    
    fig_enem.update_layout(**get_dark_layout(
        title='🎯 Nota Média no ENEM por Condição de Saneamento',
        height=500,
        showlegend=False
    ))
    fig_enem.update_yaxes(title_text='Pontuação', range=[0, 600])
    
    st.plotly_chart(fig_enem, use_container_width=True)
    
    st.markdown(f"""
    <div class="box-info">
        <strong>🎯 Impacto de ~80 pontos:</strong><br>
        Uma diferença de aproximadamente 80 pontos no ENEM pode determinar:
        <ul>
            <li>Acesso ou não a cursos competitivos (Medicina, Direito, Engenharias)</li>
            <li>Conseguir ou não bolsa integral no ProUni</li>
            <li>Entrar ou ficar de fora de uma universidade federal</li>
            <li>O rumo de toda uma vida profissional</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 6. VISÃO INTEGRADA
# ============================================
st.markdown("---")
st.markdown('<h2 class="secao-titulo">🔄 Visão Integrada: O Ciclo Completo</h2>', unsafe_allow_html=True)

# Normalização dos dados para o gráfico radar (0-100%)
renda_max = max(DADOS_DF['renda_com_saneamento'], DADOS_DF['renda_sem_saneamento'])
renda_com = (DADOS_DF['renda_com_saneamento'] / renda_max) * 100
renda_sem = (DADOS_DF['renda_sem_saneamento'] / renda_max) * 100

escol_max = max(DADOS_DF['escolaridade_com'], DADOS_DF['escolaridade_sem'])
escol_com = (DADOS_DF['escolaridade_com'] / escol_max) * 100
escol_sem = (DADOS_DF['escolaridade_sem'] / escol_max) * 100

enem_max = max(DADOS_DF['enem_com_banheiro'], DADOS_DF['enem_sem_banheiro'])
enem_com = (DADOS_DF['enem_com_banheiro'] / enem_max) * 100
enem_sem = (DADOS_DF['enem_sem_banheiro'] / enem_max) * 100

# Gráfico Radar estilo escuro
categorias = ['Saúde', 'Renda', 'Escolaridade', 'ENEM', 'Saúde']

fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=[100, renda_com, escol_com, enem_com, 100],
    theta=categorias,
    fill='toself',
    fillcolor='rgba(77, 171, 247, 0.4)',
    line=dict(color=CORES['azul'], width=3),
    name='✅ Com Saneamento',
    marker=dict(size=8, color=CORES['azul'])
))

fig_radar.add_trace(go.Scatterpolar(
    r=[88, renda_sem, escol_sem, enem_sem, 88],
    theta=categorias,
    fill='toself',
    fillcolor='rgba(255, 107, 107, 0.4)',
    line=dict(color=CORES['vermelho'], width=3),
    name='❌ Sem Saneamento',
    marker=dict(size=8, color=CORES['vermelho'])
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100],
            tickfont=dict(size=10, color=CORES['texto']),
            gridcolor=CORES['grid'],
            linecolor=CORES['grid']
        ),
        angularaxis=dict(
            tickfont=dict(size=14, color=CORES['texto'], family='Arial Black'),
            linecolor=CORES['grid'],
            gridcolor=CORES['grid']
        ),
        bgcolor=CORES['bg_escuro']
    ),
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.15,
        xanchor='center',
        x=0.5,
        font=dict(size=14, color=CORES['texto'])
    ),
    title=dict(
        text='🔍 Comparativo Geral: Indicadores Normalizados (0-100%)',
        font=dict(size=20, color=CORES['texto']),
        x=0.5
    ),
    paper_bgcolor=CORES['bg_escuro'],
    height=550,
    margin=dict(t=80, b=100)
)

st.plotly_chart(fig_radar, use_container_width=True)

# Ciclos
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="ciclo-vicioso">
        <h3 style="text-align: center; margin-bottom: 1rem;">🔻 Ciclo Vicioso</h3>
        <div class="ciclo-item">1. ❌ Falta de saneamento básico</div>
        <div class="ciclo-item">2. 🦠 Aumento de doenças</div>
        <div class="ciclo-item">3. 🏥 Mais internações e gastos</div>
        <div class="ciclo-item">4. 📉 Faltas na escola e trabalho</div>
        <div class="ciclo-item">5. 📚 Menor escolaridade</div>
        <div class="ciclo-item">6. 💸 Menor renda</div>
        <div class="ciclo-item" style="border-bottom: none;">7. 🔄 Permanece sem saneamento</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="ciclo-virtuoso">
        <h3 style="text-align: center; margin-bottom: 1rem;">🔺 Ciclo Virtuoso</h3>
        <div class="ciclo-item">1. ✅ Acesso a saneamento básico</div>
        <div class="ciclo-item">2. 💪 Redução de doenças</div>
        <div class="ciclo-item">3. 💰 Economia com saúde</div>
        <div class="ciclo-item">4. 📈 Mais frequência escolar</div>
        <div class="ciclo-item">5. 🎓 Maior escolaridade</div>
        <div class="ciclo-item">6. 💵 Maior renda</div>
        <div class="ciclo-item" style="border-bottom: none;">7. 🏠 Melhores condições de vida</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# 7. CONCLUSÕES
# ============================================
st.markdown("---")
st.markdown('<h2 class="secao-titulo">💡 Conclusões e Recomendações</h2>', unsafe_allow_html=True)

st.markdown("### Síntese dos Achados")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card-conclusao borda-saude">
        <h4>🏥 Saúde</h4>
        <p><b>{DADOS_DF['internacoes_total']:,}</b> internações e <b>{DADOS_DF['obitos']}</b> óbitos 
        poderiam ter sido evitados com saneamento adequado, gerando economia de 
        <b>R$ {DADOS_DF['custo_internacoes']:,.2f}</b> ao sistema de saúde.</p>
    </div>
    """.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card-conclusao borda-renda">
        <h4>💰 Renda</h4>
        <p>A diferença mensal de <b>R$ {DADOS_DF['diferenca_renda']:,.2f}</b> 
        representa mais de <b>R$ 13.000/ano</b> que deixam de circular na economia local, 
        perpetuando o ciclo de pobreza.</p>
    </div>
    """.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card-conclusao borda-educacao">
        <h4>🎓 Educação</h4>
        <p>O gap de <b>{DADOS_DF['diferenca_escolaridade']:.2f}</b> anos de estudo e 
        <b>{DADOS_DF['diferenca_enem']:.2f}</b> pontos no ENEM compromete 
        o futuro de milhares de jovens do DF.</p>
    </div>
    """.replace(".", ","), unsafe_allow_html=True)

st.markdown("### Recomendações")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="box-info">
        <h4>📅 Curto Prazo (1-2 anos)</h4>
        <ul>
            <li>Mapear áreas prioritárias sem cobertura</li>
            <li>Implementar soluções emergenciais de tratamento de água</li>
            <li>Intensificar campanhas de educação sanitária</li>
            <li>Aumentar fiscalização de ligações clandestinas</li>
            <li>Criar programa de subsídio para famílias de baixa renda</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="box-info">
        <h4>📅 Longo Prazo (3-10 anos)</h4>
        <ul>
            <li>Universalização do acesso à água tratada</li>
            <li>Expansão da rede de coleta e tratamento de esgoto</li>
            <li>Integração das políticas de saneamento, saúde e educação</li>
            <li>Investimento em tecnologias sustentáveis</li>
            <li>Monitoramento contínuo de indicadores</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="box-alerta">
    <h4>⚠️ A Urgência da Ação</h4>
    <p>Cada dia sem ação representa mais vidas impactadas, mais recursos desperdiçados e mais 
    oportunidades perdidas. O saneamento básico não é apenas uma questão de infraestrutura — 
    é uma questão de <b>direitos humanos</b>, <b>justiça social</b> e <b>desenvolvimento sustentável</b>.</p>
    <p style="text-align: center; font-size: 1.2rem; margin-top: 1rem;">
        <b>"Saneamento para todos não é um sonho, é uma necessidade urgente."</b>
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 8. RODAPÉ
# ============================================
st.markdown("---")
st.markdown("""
<div class="rodape">
    <h4>📚 Fontes de Dados</h4>
    <p>
        <b>DATASUS</b> - Sistema de Informações Hospitalares (SIH/SUS) - 2023<br>
        <b>IBGE</b> - Pesquisa Nacional por Amostra de Domicílios (PNAD) - 2023<br>
        <b>INEP</b> - Microdados do ENEM - 2023<br>
        <b>SINISA</b> - Sistema Nacional de Informações sobre Saneamento - 2023
    </p>
    <p style="margin-top: 1rem;">
        🔗 <a href="https://www.painelsaneamento.org.br/" target="_blank">Painel Saneamento Brasil</a>
    </p>
    <hr style="margin: 1.5rem 0; border-color: #caf0f8;">
    <div class="creditos">
        <p style="margin: 0; font-size: 1.1rem;">
            👩‍💻 <b>Desenvolvido por:</b><br>
            <span style="font-size: 1.3rem;">Bruna Cayres & Maria Eduarda</span>
        </p>
    </div>
    <p style="color: #666; font-size: 0.9rem; margin-top: 1rem;">
        💧 Dashboard desenvolvido para análise da disparidade socioeconômica causada pela falta de saneamento básico no Distrito Federal<br>
        🗓️ Dados referentes ao ano de 2023 | Última atualização: Dezembro/2024
    </p>
</div>
""", unsafe_allow_html=True)
