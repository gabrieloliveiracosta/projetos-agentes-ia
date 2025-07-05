
import { useEffect, useState } from 'react';

type Carteira = {
  pesos: Record<string, number>;
  retorno_anualizado: number;
  volatilidade_anualizada: number;
  sharpe_ratio: number;
};

function PortfolioResult() {
  const [data, setData] = useState<Carteira | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem('carteira');
    if (stored) {
      setData(JSON.parse(stored));
    }
  }, []);

  if (!data) return <p className="p-6">Carregando...</p>;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Carteira ótima gerada</h2>

      <table className="w-full text-left border mb-6">
        <thead className="bg-gray-100">
          <tr><th className="p-2">Produto</th><th className="p-2">Peso</th></tr>
        </thead>
        <tbody>
          {Object.entries(data.pesos).map(([prod, peso]) => (
            <tr key={prod} className="border-t">
              <td className="p-2">{prod}</td>
              <td className="p-2">{(peso*100).toFixed(2)}%</td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="space-y-2">
        <p><b>Retorno anualizado:</b> {(data.retorno_anualizado*100).toFixed(2)}%</p>
        <p><b>Volatilidade anualizada:</b> {(data.volatilidade_anualizada*100).toFixed(2)}%</p>
        <p><b>Sharpe Ratio:</b> {data.sharpe_ratio.toFixed(2)}</p>
      </div>
    </div>
  );
}

export default PortfolioResult;
