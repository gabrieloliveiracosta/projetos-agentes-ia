import pandas as pd
import numpy as np
from scipy.optimize import minimize


class AdvisoryAgent3:
    def __init__(self, retornos_diarios: pd.DataFrame, classes: dict, limites_por_classe: dict):
        """
        retornos_diarios: DataFrame com retornos diários dos produtos (produtos como colunas)
        classes: dicionário {produto: classe}
        limites_por_classe: dicionário {classe: {'minimo': x, 'maximo': y}}
        """
        self.retornos = retornos_diarios
        self.classes = classes
        self.limites_classe = limites_por_classe
        self.resultado = None
        self.retorno_carteira = None
        self.volatilidade_carteira = None
        self.sharpe_carteira = None

    def otimizar_carteira(self, vol_target=0.04, tolerancia=0.2, penalizar_concentracao=True, alpha=0.01):
        """
        vol_target: volatilidade alvo (ex: 0.04 = 4%)
        tolerancia: tolerância percentual para a volatilidade alvo (ex: 0.2 = ±20%)
        penalizar_concentracao: se True, adiciona leve penalidade para evitar concentração em poucos ativos
        alpha: peso da penalidade (quanto maior, mais força a diversificação)
        """
        produtos = list(self.retornos.columns)
        n = len(produtos)
        cov_matrix = self.retornos.cov() * 252  # anualiza covariância
        retornos_medios = self.retornos.mean() * 252  # anualiza retornos médios

        # -----------------------
        # Restrições por classe
        # -----------------------
        def classe_constraints():
            constraints = []
            for classe, lim in self.limites_classe.items():
                indices = [i for i, prod in enumerate(produtos) if self.classes[prod] == classe]
                # mínimo da classe
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda x, idx=indices, minimo=lim['minimo']:
                        np.sum(x[idx]) - minimo
                })
                # máximo da classe
                constraints.append({
                    'type': 'ineq',
                    'fun': lambda x, idx=indices, maximo=lim['maximo']:
                        maximo - np.sum(x[idx])
                })
            return constraints

        # -----------------------
        # Restrições gerais
        # -----------------------
        constraints = (
            [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}] +  # Soma dos pesos = 1
            classe_constraints() +  # Limites por classe
            [  # Volatilidade dentro da faixa
                {'type': 'ineq', 'fun': lambda x: (1 + tolerancia) * vol_target - np.sqrt(np.dot(x.T, np.dot(cov_matrix, x)))},
                {'type': 'ineq', 'fun': lambda x: np.sqrt(np.dot(x.T, np.dot(cov_matrix, x))) - (1 - tolerancia) * vol_target}
            ]
        )

        bounds = [(0, 1) for _ in range(n)]  # Pesos individuais [0%, 100%]

        # -----------------------
        # Função objetivo: Max Sharpe
        # -----------------------
        def objetivo(x):
            retorno = np.dot(x, retornos_medios)
            vol = np.sqrt(np.dot(x.T, np.dot(cov_matrix, x)))
            sharpe = retorno / vol if vol > 0 else 0  # rf = 0
            penalty = alpha * np.sum(x**2) if penalizar_concentracao else 0
            return -sharpe + penalty  # Negativo porque minimize()

        # -----------------------
        # Otimização
        # -----------------------
        x0 = np.array([1 / n] * n)  # Alocação inicial igualitária
        resultado = minimize(objetivo, x0, method='SLSQP', bounds=bounds, constraints=constraints)

        if resultado.success:
            self.resultado = pd.Series(resultado.x, index=produtos)
            self.retorno_carteira = np.dot(self.resultado.values, retornos_medios)
            self.volatilidade_carteira = np.sqrt(np.dot(self.resultado.values.T, np.dot(cov_matrix, self.resultado.values)))
            self.sharpe_carteira = self.retorno_carteira / self.volatilidade_carteira if self.volatilidade_carteira > 0 else np.nan
        else:
            raise ValueError("Otimização falhou: " + resultado.message)

    def obter_pesos_otimizados(self):
        return self.resultado

    def obter_retorno_carteira(self):
        return self.retorno_carteira

    def obter_volatilidade_carteira(self):
        return self.volatilidade_carteira

    def obter_sharpe_carteira(self):
        return self.sharpe_carteira
