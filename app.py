"""
Interface Web para Weighted Interval Scheduling
Agendador Inteligente de 1 Sala
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from io import StringIO
from algorithm import (
    Aula, 
    converter_hora_para_minutos, 
    weighted_interval_scheduling
)

# Configuração da página
st.set_page_config(
    page_title="Agendador Inteligente",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Agendador Inteligente de Aulas")
st.markdown("**Weighted Interval Scheduling com Programação Dinâmica**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Sobre")
    st.info("""
    **Weighted Interval Scheduling**
    
    Encontra o conjunto ÓTIMO de aulas 
    que não se sobrepõem em UMA sala,
    maximizando a prioridade total.
    
    Aulas com conflito são **rejeitadas**
    (não podem estar na mesma sala).
    """)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["Entrada", "Processamento", "Resultados", "Documentação"]
)

# ============== TAB 1: ENTRADA ==============
with tab1:
    st.header("Inserir Dados das Aulas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Opção 1: Upload CSV")
        uploaded_file = st.file_uploader(
            "Escolha um arquivo CSV",
            type="csv",
            help="Formato: nome,inicio,fim,prioridade"
        )
    
    with col2:
        st.subheader("Opção 2: Adicionar Manualmente")
        usar_manual = st.checkbox("Adicionar aulas manualmente")
    
    # Exemplo de CSV
    with st.expander("Ver exemplo de formato CSV"):
        exemplo_csv = """nome,inicio,fim,prioridade
Python Avançado,08:00,10:00,10
Java Básico,08:30,09:30,3
C++ Essencial,09:00,11:00,8
Web Dev,10:00,11:00,2
Machine Learning,10:30,12:00,9"""
        st.code(exemplo_csv, language="csv")
        st.download_button(
            label="Baixar Exemplo CSV",
            data=exemplo_csv,
            file_name="exemplo-aulas.csv",
            mime="text/csv"
        )
    
    # Processa upload
    aulas_lista = []
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            for idx, row in df.iterrows():
                try:
                    aula = Aula(
                        id=idx + 1,
                        nome=row['nome'].strip(),
                        inicio=converter_hora_para_minutos(row['inicio'].strip()),
                        fim=converter_hora_para_minutos(row['fim'].strip()),
                        prioridade=int(row['prioridade'])
                    )
                    aulas_lista.append(aula)
                except Exception as e:
                    st.error(f"Erro na linha {idx + 2}: {e}")
            
            st.success(f"{len(aulas_lista)} aulas carregadas!")
            
            # Mostra tabela
            st.subheader("Aulas Carregadas:")
            df_display = pd.DataFrame([
                {
                    "Nome": aula.nome,
                    "Início": f"{aula.inicio//60:02d}:{aula.inicio%60:02d}",
                    "Fim": f"{aula.fim//60:02d}:{aula.fim%60:02d}",
                    "Duração": f"{(aula.fim - aula.inicio)}min",
                    "Prioridade": aula.prioridade
                }
                for aula in aulas_lista
            ])
            st.dataframe(df_display, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")
    
    elif usar_manual:
        st.subheader("Adicionar Aulas Manualmente")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            nome_aula = st.text_input("Nome da Aula")
        with col2:
            hora_inicio = st.time_input("Hora Início", value=None)
        with col3:
            hora_fim = st.time_input("Hora Fim", value=None)
        with col4:
            prioridade = st.slider("Prioridade", 1, 10, 5)
        
        if st.button("Adicionar Aula"):
            if nome_aula and hora_inicio and hora_fim:
                try:
                    aula = Aula(
                        id=1,
                        nome=nome_aula,
                        inicio=hora_inicio.hour * 60 + hora_inicio.minute,
                        fim=hora_fim.hour * 60 + hora_fim.minute,
                        prioridade=prioridade
                    )
                    if 'aulas_manual' not in st.session_state:
                        st.session_state.aulas_manual = []
                    st.session_state.aulas_manual.append(aula)
                    st.success(f" {nome_aula} adicionada!")
                except Exception as e:
                    st.error(f"Erro: {e}")
        
        if 'aulas_manual' in st.session_state and st.session_state.aulas_manual:
            st.subheader("Aulas Adicionadas:")
            for i, aula in enumerate(st.session_state.aulas_manual):
                h_ini = aula.inicio // 60
                m_ini = aula.inicio % 60
                h_fim = aula.fim // 60
                m_fim = aula.fim % 60
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{aula.nome} ({h_ini:02d}:{m_ini:02d}-{h_fim:02d}:{m_fim:02d}) P:{aula.prioridade}")
                with col2:
                    if st.button("❌", key=f"remove_{i}"):
                        st.session_state.aulas_manual.pop(i)
                        st.rerun()
            
            aulas_lista = st.session_state.aulas_manual
    
    # Armazena em session_state
    if aulas_lista:
        st.session_state.aulas_lista = aulas_lista

# ============== TAB 2: PROCESSAMENTO ==============
with tab2:
    st.header("Executar Algoritmo")
    
    if 'aulas_lista' in st.session_state and st.session_state.aulas_lista:
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Total de Aulas",
                len(st.session_state.aulas_lista),
                help="Número de aulas a processar"
            )
        
        with col2:
            st.metric(
                "Sala",
                "1",
                help="Aulas serão agendadas em UMA sala"
            )
        
        st.markdown("---")
        
        if st.button("EXECUTAR ALGORITMO", use_container_width=True):
            st.info("Processando com Programação Dinâmica...")
            
            # Executa algoritmo WIS
            aulas_selecionadas, prioridade_total = weighted_interval_scheduling(
                st.session_state.aulas_lista
            )
            
            # Armazena resultados
            st.session_state.aulas_selecionadas = aulas_selecionadas
            st.session_state.prioridade_total = prioridade_total
            
            st.success("Algoritmo executado com sucesso!")
            
            # Mostra resumo
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Aulas Agendadas",
                    len(aulas_selecionadas),
                    f"{len(st.session_state.aulas_lista) - len(aulas_selecionadas)} rejeitadas"
                )
            
            with col2:
                st.metric(
                    "Prioridade Total",
                    prioridade_total,
                    help="Soma das prioridades das aulas agendadas"
                )
            
            with col3:
                taxa = (len(aulas_selecionadas) / len(st.session_state.aulas_lista)) * 100
                st.metric(
                    "Aulas Agendadas %",
                    f"{taxa:.1f}%",
                    help="Percentual de aulas sem conflito"
                )
    
    else:
        st.warning("Por favor, carregue as aulas primeiro na aba 'Entrada'")

# ============== TAB 3: RESULTADOS ==============
with tab3:
    st.header("Resultados do Agendamento")
    
    if 'aulas_selecionadas' in st.session_state:
        
        # Aulas selecionadas
        st.subheader("Aulas Agendadas")
        
        df_agendadas = pd.DataFrame([
            {
                "Aula": aula.nome,
                "Início": f"{aula.inicio//60:02d}:{aula.inicio%60:02d}",
                "Fim": f"{aula.fim//60:02d}:{aula.fim%60:02d}",
                "Duração": f"{(aula.fim - aula.inicio)}min",
                "Prioridade": aula.prioridade
            }
            for aula in st.session_state.aulas_selecionadas
        ])
        
        st.dataframe(df_agendadas, use_container_width=True)
        
        # Aulas rejeitadas
        aulas_rejeitadas = [
            a for a in st.session_state.aulas_lista 
            if a not in st.session_state.aulas_selecionadas
        ]
        
        if aulas_rejeitadas:
            st.subheader("Aulas Rejeitadas (conflitam com agendadas)")
            df_rejeitadas = pd.DataFrame([
                {
                    "Aula": aula.nome,
                    "Início": f"{aula.inicio//60:02d}:{aula.inicio%60:02d}",
                    "Fim": f"{aula.fim//60:02d}:{aula.fim%60:02d}",
                    "Duração": f"{(aula.fim - aula.inicio)}min",
                    "Prioridade": aula.prioridade
                }
                for aula in aulas_rejeitadas
            ])
            st.dataframe(df_rejeitadas, use_container_width=True)
        
        st.markdown("---")
        
        # Visualização
        st.subheader("Timeline ")
        
        fig = go.Figure()
        
        for aula in sorted(st.session_state.aulas_selecionadas, key=lambda a: a.inicio):
            h_ini = aula.inicio // 60
            m_ini = aula.inicio % 60
            h_fim = aula.fim // 60
            m_fim = aula.fim % 60
            
            fig.add_trace(go.Bar(
                y=["Sala 1"],
                x=[aula.fim - aula.inicio],
                base=aula.inicio,
                name=aula.nome,
                text=f"{aula.nome}<br>P:{aula.prioridade}",
                textposition="inside",
                orientation="h",
                marker=dict(color='#636EFA'),
                hovertemplate=f"<b>{aula.nome}</b><br>" +
                              f"{h_ini:02d}:{m_ini:02d}-{h_fim:02d}:{m_fim:02d}<br>" +
                              f"Prioridade: {aula.prioridade}<extra></extra>"
            ))
        
        min_minutos = min(a.inicio for a in st.session_state.aulas_selecionadas)
        max_minutos = max(a.fim for a in st.session_state.aulas_selecionadas)
        
        # Cria os marcadores de hora em hora (saltos de 60 minutos)
        marcadores_valores = list(range((min_minutos // 60) * 60, max_minutos + 60, 60))
        marcadores_textos = [f"{v // 60:02d}:00" for v in marcadores_valores]

        fig.update_layout(
            barmode='overlay',
            height=250,
            title="Aulas Agendadas (sem sobreposição)",
            xaxis_title="Horário",
            yaxis_title="",
            hovermode='closest',
            showlegend=False,
            xaxis=dict(
                tickmode='array',
                tickvals=marcadores_valores,
                ticktext=marcadores_textos
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Download
        st.subheader("Exportar Resultados")
        
        resultado_json = {
            "prioridade_total": st.session_state.prioridade_total,
            "aulas_selecionadas": [
                {
                    "nome": a.nome,
                    "inicio": f"{a.inicio//60:02d}:{a.inicio%60:02d}",
                    "fim": f"{a.fim//60:02d}:{a.fim%60:02d}",
                    "prioridade": a.prioridade
                }
                for a in st.session_state.aulas_selecionadas
            ]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "Baixar em JSON",
                json.dumps(resultado_json, indent=2, ensure_ascii=False),
                "agendamento.json",
                "application/json"
            )
        
        with col2:
            csv_result = df_agendadas.to_csv(index=False)
            st.download_button(
                "Baixar em CSV",
                csv_result,
                "agendamento.csv",
                "text/csv"
            )
    
    else:
        st.info("💡 Execute o algoritmo na aba 'Processamento' para ver os resultados")

# ============== TAB 4: DOCUMENTAÇÃO ==============
with tab4:
    st.header("Documentação")
    
    st.subheader("O que é Weighted Interval Scheduling?")
    st.markdown("""
    **Weighted Interval Scheduling** é um problema clássico de otimização:
    
    **Entrada:** Uma lista de intervalos (aulas), cada um com:
    - Hora de início e término  
    - Um "peso" ou prioridade
    
    **Objetivo:** Selecionar o maior subconjunto de intervalos que:
    - Não se sobrepõem (sem conflitos)
    - Maximizam a soma das prioridades
    
    **Método:** Programação Dinâmica
    - Ordena os intervalos por tempo de término
    - Constrói uma tabela DP onde cada célula armazena a solução ótima
    - Reconstrói a solução fazendo backtracking
    """)
    
    st.subheader("Complexidade")
    st.markdown("""
    - **Tempo:** O(n log n) - dominado pela ordenação
    - **Espaço:** O(n) - para armazenar a tabela DP
    
    Onde n = número de aulas
    """)
    
    st.subheader("Por que aulas são rejeitadas?")
    st.markdown("""
    Uma aula é **rejeitada** quando:
    - Seu horário **conflita** com uma aula de **maior ou igual prioridade** que já foi agendada
    - O algoritmo escolhe maximizar a prioridade total, não o número de aulas
    
    **Exemplo:**
    - Aula A: 08:00-09:00, Prioridade 10 - Agendada
    - Aula B: 08:30-09:30, Prioridade 3  - Rejeitada (conflita com A e A tem maior prioridade)
    """)

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><small>Desenvolvido usando Programação Dinâmica</small></p>
</div>
""", unsafe_allow_html=True)