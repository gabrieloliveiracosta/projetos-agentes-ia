import pandas as pd
import numpy as np

class AdvisoryAgent2:
    def __init__(self, produtos_df: pd.DataFrame):
        """
        :param produtos_df: DataFrame retornado pelo AgenteProdutos com MultiIndex (produto, classe)
        """
        # Detecta automaticamente a coluna 'periodo' no MultiIndex e define como índice
        periodo_col = [col for col in produtos_df.columns if col[0] == "periodo"][0]
        self.produtos_df = produtos_df.set_index(periodo_col)

        # Simplifica as colunas para usar apenas o nome do produto
        self.produtos_df.columns = [col[0] for col in self.produtos_df.columns]

        self.volatilidade = {}
        self.retorno_acumulado = {}
        self.corr_matrix = pd.DataFrame()

    def calcular_metricas(self):
        # Retorno acumulado (produto dos retornos diários menos 1)
        self.retorno_acumulado = self.produtos_df.add(1).prod() - 1

        # Volatilidade anualizada (std diário * sqrt(252))
        volatilidade_diaria = self.produtos_df.std()
        self.volatilidade = volatilidade_diaria * np.sqrt(252)

        # Matriz de correlação dos retornos diários
        self.corr_matrix = self.produtos_df.corr()

    def obter_volatilidade(self):
        return self.volatilidade

    def obter_retorno_acumulado(self):
        return self.retorno_acumulado

    def obter_correlacao(self):
        return self.corr_matrix
