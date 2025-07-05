import pandas as pd

class AgenteProdutos:
    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self.dados = None
        self.produtos = []
        self.classes = {}

    def carregar_dados(self):
        # Lê a planilha com MultiIndex nas colunas (primeira linha: nome do produto, segunda: classe)
        self.dados = pd.read_excel(self.caminho_arquivo, header=[0, 1])

        # Renomeia a primeira coluna (índice do período)
        self.dados.rename(columns={self.dados.columns[0]: ('periodo', '')}, inplace=True)

        # Salva lista de produtos (excluindo a coluna de período)
        self.produtos = [col[0] for col in self.dados.columns if col[0] != 'periodo']

        # Cria dicionário: produto ➝ classe
        self.classes = {col[0]: col[1] for col in self.dados.columns if col[0] != 'periodo'}

    def obter_dados(self):
        return self.dados

    def obter_produtos(self):
        return self.produtos

    def obter_classes(self):
        return self.classes

# Exemplo de uso
if __name__ == "__main__":
    agente = AgenteProdutos("produtos.xlsx")
    agente.carregar_dados()

    # Acesso aos dados
    df = agente.obter_dados()
    produtos = agente.obter_produtos()
    classes = agente.obter_classes()

    print("Produtos disponíveis:", produtos)
    print("Classes de produtos:", classes)
    print("Amostra dos dados:")
    print(df.head())
