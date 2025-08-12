import streamlit as st
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Sua Vida em Semanas",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

def calcular_semanas_vividas(data_nascimento, data_atual=None):
    """Calcula quantas semanas foram vividas desde o nascimento"""
    if data_atual is None:
        data_atual = datetime.now()
    
    delta = data_atual - data_nascimento
    semanas_vividas = delta.days // 7
    return semanas_vividas

def criar_grid_vida(semanas_vividas, expectativa_vida=80):
    """Cria o grid da vida em semanas"""
    total_semanas = expectativa_vida * 52
    semanas_por_linha = 52  # Um ano por linha
    
    # Criar matriz
    linhas = expectativa_vida
    grid = []
    
    for ano in range(linhas):
        linha = []
        for semana in range(semanas_por_linha):
            semana_absoluta = ano * semanas_por_linha + semana
            
            if semana_absoluta < semanas_vividas:
                status = 'vivida'
            else:
                status = 'futura'
                
            linha.append({
                'ano': ano,
                'semana': semana,
                'semana_absoluta': semana_absoluta,
                'status': status
            })
        grid.append(linha)
    
    return grid

def criar_visualizacao_plotly(grid_data, semanas_vividas, expectativa_vida):
    """Cria visualização usando Plotly"""
    # Preparar dados para o heatmap
    z_data = []
    hover_text = []
    
    for ano_data in grid_data:
        z_linha = []
        hover_linha = []
        for semana_data in ano_data:
            if semana_data['status'] == 'vivida':
                z_linha.append(1)
                hover_linha.append(f"Ano {semana_data['ano'] + 1}, Semana {semana_data['semana'] + 1}<br>Status: Vivida")
            else:
                z_linha.append(0)
                hover_linha.append(f"Ano {semana_data['ano'] + 1}, Semana {semana_data['semana'] + 1}<br>Status: Futura")
        
        z_data.append(z_linha)
        hover_text.append(hover_linha)
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        text=hover_text,
        hovertemplate='%{text}<extra></extra>',
        colorscale=[[0, '#f0f0f0'], [1, '#2E86AB']],
        showscale=False,
        xgap=1,
        ygap=1
    ))
    
    fig.update_layout(
        title={
            'text': f"Sua Vida em Semanas - {semanas_vividas:,} semanas vividas de {expectativa_vida * 52:,} total",
            'x': 0.5,
            'font': {'size': 20}
        },
        xaxis_title="Semanas do Ano",
        yaxis_title="Anos de Vida",
        height=600,
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 12, 25, 38, 51],
            ticktext=['Jan', 'Abr', 'Jul', 'Out', 'Dez']
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(0, expectativa_vida, 10)),
            ticktext=[str(i+1) for i in range(0, expectativa_vida, 10)]
        )
    )
    
    return fig

def main():
    st.title("📅 Sua Vida em Semanas")
    st.markdown("""
    Esta visualização mostra toda uma vida humana representada em semanas. 
    Cada quadradinho representa uma semana da sua vida. Os quadrados azuis 
    são as semanas que você já viveu, e os cinzas são as que ainda estão por vir.
    """)
    
    # Sidebar para inputs
    st.sidebar.header("⚙️ Configurações")
    
    # Input da data de nascimento
    data_nascimento = st.sidebar.date_input(
        "📅 Data de Nascimento",
        value=datetime(1990, 1, 1),
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now()
    )
    
    # Input da expectativa de vida
    expectativa_vida = st.sidebar.slider(
        "📊 Expectativa de Vida (anos)",
        min_value=50,
        max_value=100,
        value=80,
        step=1
    )
    
    # Converter para datetime
    data_nascimento = datetime.combine(data_nascimento, datetime.min.time())
    
    # Calcular semanas vividas
    semanas_vividas = calcular_semanas_vividas(data_nascimento)
    
    # Criar grid
    grid_data = criar_grid_vida(semanas_vividas, expectativa_vida)
    
    # Estatísticas
    col1, col2, col3, col4 = st.columns(4)
    
    total_semanas = expectativa_vida * 52
    semanas_restantes = total_semanas - semanas_vividas
    porcentagem_vivida = (semanas_vividas / total_semanas) * 100
    idade_atual = semanas_vividas / 52
    
    with col1:
        st.metric("🗓️ Semanas Vividas", f"{semanas_vividas:,}")
    
    with col2:
        st.metric("⏳ Semanas Restantes", f"{semanas_restantes:,}")
    
    with col3:
        st.metric("📈 Porcentagem da Vida", f"{porcentagem_vivida:.1f}%")
    
    with col4:
        st.metric("🎂 Idade Atual", f"{idade_atual:.1f} anos")
    
    # Visualização principal
    st.subheader("🎯 Visualização da Vida")
    
    fig = criar_visualizacao_plotly(grid_data, semanas_vividas, expectativa_vida)
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights e reflexões
    st.subheader("💭 Reflexões")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Perspectiva Temporal:**
        - Você já viveu {semanas_vividas:,} semanas
        - Restam aproximadamente {semanas_restantes:,} semanas
        - Isso representa {semanas_restantes/52:.1f} anos pela frente
        """)
    
    with col2:
        if porcentagem_vivida < 25:
            fase = "início da jornada"
            emoji = "🌱"
        elif porcentagem_vivida < 50:
            fase = "crescimento e descobertas"
            emoji = "🌿"
        elif porcentagem_vivida < 75:
            fase = "maturidade e experiência"
            emoji = "🌳"
        else:
            fase = "sabedoria e reflexão"
            emoji = "🍂"
        
        st.success(f"""
        **{emoji} Fase da Vida:**
        Você está na fase de {fase}.
        
        **Dica:** Cada semana é preciosa e única. 
        Use este tempo de forma consciente!
        """)
    
    # Análise detalhada
    st.subheader("📊 Análise Detalhada")
    
    # Criar DataFrame para análise
    anos_dados = []
    for i in range(0, min(expectativa_vida, int(idade_atual) + 10), 10):
        inicio_ano = i
        fim_ano = min(i + 10, expectativa_vida)
        semanas_periodo = (fim_ano - inicio_ano) * 52
        
        semanas_vividas_periodo = max(0, min(semanas_vividas - inicio_ano * 52, semanas_periodo))
        porcentagem_periodo = (semanas_vividas_periodo / semanas_periodo) * 100 if semanas_periodo > 0 else 0
        
        anos_dados.append({
            'Período': f"{inicio_ano}-{fim_ano-1} anos",
            'Semanas do Período': semanas_periodo,
            'Semanas Vividas': int(semanas_vividas_periodo),
            'Progresso (%)': f"{porcentagem_periodo:.1f}%"
        })
    
    df_analise = pd.DataFrame(anos_dados)
    st.dataframe(df_analise, use_container_width=True)
    
    # Gráfico de barras do progresso por década
    fig_barras = px.bar(
        df_analise,
        x='Período',
        y='Semanas Vividas',
        title='Semanas Vividas por Período da Vida',
        color='Semanas Vividas',
        color_continuous_scale='Blues'
    )
    
    fig_barras.update_layout(height=400)
    st.plotly_chart(fig_barras, use_container_width=True)
    
    # Seção de exportação
    st.subheader("💾 Exportar Dados")
    
    if st.button("📥 Gerar Relatório CSV"):
        # Criar dados detalhados para CSV
        dados_csv = []
        for ano, linha in enumerate(grid_data):
            for semana_data in linha:
                dados_csv.append({
                    'Ano': semana_data['ano'] + 1,
                    'Semana_do_Ano': semana_data['semana'] + 1,
                    'Semana_Absoluta': semana_data['semana_absoluta'] + 1,
                    'Status': semana_data['status'],
                    'Data_Aproximada': (data_nascimento + timedelta(weeks=semana_data['semana_absoluta'])).strftime('%Y-%m-%d')
                })
        
        df_csv = pd.DataFrame(dados_csv)
        csv = df_csv.to_csv(index=False)
        
        st.download_button(
            label="📄 Download CSV",
            data=csv,
            file_name=f"vida_em_semanas_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.success("Relatório gerado! Use o botão acima para fazer o download.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        💡 <em>"Hoje é o futuro de ontem, sem parar, todo dia menos um."</em> - Caio<br>
        Cada quadradinho azul representa uma semana única da sua jornada. Valorize cada momento! ⏰
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()