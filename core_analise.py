# Este arquivo encapsula toda a lógica do Pandas. Ele limpa espaços em branco, remove nulos e categoriza os dados de forma agnóstica.

import pandas as pd

class MotorAnalise:
    def __init__(self, arquivo):
        self.df = self._carregar_arquivo(arquivo)
        self._limpar_dados()

    def _carregar_arquivo(self, arquivo):
        """Lê dinamicamente formatos Excel ou CSV"""
        if hasattr(arquivo, 'name') and arquivo.name.endswith('.csv'):
            return pd.read_csv(arquivo)
        return pd.read_excel(arquivo)

    def _limpar_dados(self):
        """Ajusta textos e remove dados completamente nulos"""
        # Remove linhas totalmente vazias
        self.df.dropna(how='all', inplace=True)
        # Limpa espaços extras nos nomes das colunas
        self.df.columns = [str(col).strip() for col in self.df.columns]
        
        # Remove espaços extras de colunas de texto
        for col in self.select_colunas_texto():
            self.df[col] = self.df[col].astype(str).str.strip()

    def select_colunas_texto(self):
        """Retorna colunas categóricas (Texto)"""
        return self.df.select_dtypes(include=['object', 'category']).columns.tolist()

    def select_colunas_numericas(self):
        """Retorna colunas quantitativas (Números)"""
        return self.df.select_dtypes(include=['number']).columns.tolist()

    def filtrar_dados(self, dicionario_filtros):
        """Aplica múltiplos filtros simultâneos de forma dinâmica"""
        df_filtrado = self.df.copy()
        for coluna, valores in dicionario_filtros.items():
            if valores:  # Só filtra se o usuário escolheu algo
                df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]
        return df_filtrado
