import pandas as pd

def processar_metricas_ti():
    # Dados de simulação para o painel não iniciar vazio
    colunas = ['Chamado', 'Tipo', 'Sistema', 'Analista', 'Tempo_Resolucao_Min', 'Prazo_SLA_Min']
    
    linhas = [
        ['INC-001', 'Incidente', 'E-mail Corporativo', 'Ana Souza', 45, 120],
        ['REQ-002', 'Requisição', 'Reset de Senha', 'Bruno Costa', 15, 30],
        ['INC-003', 'Incidente', 'ERP Protheus', 'Ana Souza', 280, 240], 
        ['REQ-004', 'Requisição', 'Acesso à Rede', 'Carlos Melo', 60, 60],
        ['INC-005', 'Incidente', 'Internet/Link', 'Carlos Melo', 190, 180], 
        ['INC-006', 'Incidente', 'ERP Protheus', 'Ana Souza', 110, 240],
        ['REQ-007', 'Requisição', 'Reset de Senha', 'Bruno Costa', 5, 30],
        ['INC-008', 'Incidente', 'E-mail Corporativo', 'Carlos Melo', 35, 120]
    ]
    
    df = pd.DataFrame(linhas, columns=colunas)
    
    # Cria a coluna de status do SLA
    df['Status_SLA'] = df.apply(
        lambda row: 'Dentro do Prazo' if row['Tempo_Resolucao_Min'] <= row['Prazo_SLA_Min'] else 'Estourado', 
        axis=1
    )
    
    # Tabelas auxiliares apenas para manter a compatibilidade
    volumetria_sistema = df.groupby('Sistema').size().reset_index(name='Total_Chamados')
    desempenho_analistas = df.groupby('Analista').size().reset_index(name='Chamados_Resolvidos')
    indicador_sla = df.groupby('Status_SLA').size().reset_index(name='Quantidade')
    
    return df, volumetria_sistema, desempenho_analistas, indicador_sla
