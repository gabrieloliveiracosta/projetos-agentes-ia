
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const randVols = [3.0, 3.5, 4.0, 4.5, 5.0];

function InvestorProfile() {
  const navigate = useNavigate();
  const [vol, setVol] = useState(randVols[Math.floor(Math.random() * randVols.length)]);

  const gerarCarteira = async () => {
    const res = await fetch('http://localhost:8000/gerar_carteira', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ vol_target: vol / 100 })
    });
    const data = await res.json();
    localStorage.setItem('carteira', JSON.stringify(data));
    navigate('/carteira');
  };

  return (
    <div className="max-w-xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-2">Seu perfil de investidor é <span className="text-red-600">Moderado</span></h2>
      <p className="mb-6">Volatilidade-alvo inicial sugerida: <b>{vol}%</b></p>

      <label className="block mb-2 font-semibold">Ajustar volatilidade ({vol}%)</label>
      <input
        type="range"
        min="3"
        max="5"
        step="0.5"
        value={vol}
        onChange={e => setVol(parseFloat(e.target.value))}
        className="w-full"
      />

      <button
        className="mt-8 bg-red-600 text-white px-6 py-2 rounded"
        onClick={gerarCarteira}
      >
        Gerar Carteira
      </button>
    </div>
  );
}

export default InvestorProfile;
