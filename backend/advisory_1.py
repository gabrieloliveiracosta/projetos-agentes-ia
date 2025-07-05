import pandas as pd

class AdvisoryAgent1:
    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo
        self.pesos_alvo = {}
        self.limites = {}

    def carregar_pesos(self):
        # Lê a planilha sem cabeçalho
        df = pd.read_excel(self.caminho_arquivo, header=None, names=["classe", "peso_alvo"])

        # Converte os pesos para fração (caso estejam em %)
        df["peso_alvo"] = df["peso_alvo"].apply(lambda x: x / 100 if x > 1 else x)

        # Cria dicionário: classe ➝ peso alvo
        self.pesos_alvo = dict(zip(df["classe"], df["peso_alvo"]))

    def calcular_limites(self):
        # Para cada classe, calcula os limites mínimo e máximo
        for classe, peso in self.pesos_alvo.items():
            minimo = max(0.0, peso - 0.5 * peso)
            maximo = min(1.0, peso + 0.5 * peso)
            self.limites[classe] = {"minimo": minimo, "maximo": maximo}

    def obter_pesos_alvo(self):
        return self.pesos_alvo

    def obter_limites(self):
        return self.limites

# Exemplo de uso
if __name__ == "__main__":
    advisory1 = AdvisoryAgent1("pesos.xlsx")
    advisory1.carregar_pesos()
    advisory1.calcular_limites()

    print("Pesos alvo por classe:")
    for classe, peso in advisory1.obter_pesos_alvo().items():
        print(f"{classe}: {peso:.2%}")

    print("\nLimites por classe:")
    for classe, lim in advisory1.obter_limites().items():
        print(f"{classe}: mínimo = {lim['minimo']:.2%}, máximo = {lim['maximo']:.2%}")
