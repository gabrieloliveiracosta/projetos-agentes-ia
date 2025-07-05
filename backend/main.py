
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from produtos_1 import AgenteProdutos
from advisory_1 import AdvisoryAgent1
from advisory_2 import AdvisoryAgent2
from advisory_3 import AdvisoryAgent3

app = FastAPI(title="selfIA Backend", version="0.1.0")

class CarteiraRequest(BaseModel):
    vol_target: float  # e.g. 0.04 for 4%

@app.post("/gerar_carteira")
def gerar_carteira(req: CarteiraRequest):
    """Gera uma carteira ótima dado um alvo de volatilidade uniforme entre 3% e 5%."""
    try:
        # 1) carregar dados
        prod_agent = AgenteProdutos("produtos.xlsx")
        prod_agent.carregar_dados()
        df_produtos = prod_agent.obter_dados()
        classes_produto = prod_agent.obter_classes()

        adv1 = AdvisoryAgent1("pesos.xlsx")
        adv1.carregar_pesos()
        adv1.calcular_limites()
        limites_classe = adv1.obter_limites()

        adv2 = AdvisoryAgent2(df_produtos)
        adv2.calcular_metricas()
        retornos_diarios = adv2.produtos_df

        # 2) otimizar
        adv3 = AdvisoryAgent3(retornos_diarios, classes_produto, limites_classe)
        adv3.otimizar_carteira(
            vol_target=req.vol_target,
            penalizar_concentracao=True,
            alpha=0.01
        )

        pesos = adv3.obter_pesos_otimizados().round(4).to_dict()

        return {
            "pesos": pesos,
            "retorno_anualizado": round(adv3.obter_retorno_carteira(), 4),
            "volatilidade_anualizada": round(adv3.obter_volatilidade_carteira(), 4),
            "sharpe_ratio": round(adv3.obter_sharpe_carteira(), 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
