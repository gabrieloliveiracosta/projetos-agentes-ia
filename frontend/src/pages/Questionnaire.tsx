
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

function Questionnaire() {
  const navigate = useNavigate();
  const [stepComplete, setStepComplete] = useState(false);

  // perguntas dummy
  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Perguntas comportamentais</h2>

      <div className="space-y-6">
        <div>
          <p className="font-semibold">1. Como você se sente quando o mercado cai 10%?</p>
          <div className="space-y-1 mt-2">
            <label className="block"><input type="radio" name="q1" onChange={() => setStepComplete(true)}/> Fico tranquilo</label>
            <label className="block"><input type="radio" name="q1" onChange={() => setStepComplete(true)}/> Fico um pouco preocupado</label>
            <label className="block"><input type="radio" name="q1" onChange={() => setStepComplete(true)}/> Vendo tudo imediatamente</label>
          </div>
        </div>

        <div>
          <p className="font-semibold">2. Por quanto tempo você pretende investir?</p>
          <div className="space-y-1 mt-2">
            <label className="block"><input type="radio" name="q2" /> Menos de 1 ano</label>
            <label className="block"><input type="radio" name="q2" /> 1 a 5 anos</label>
            <label className="block"><input type="radio" name="q2" /> Mais de 5 anos</label>
          </div>
        </div>

        <div>
          <p className="font-semibold">3. Você prefere estabilidade ou retorno potencial maior?</p>
          <div className="space-y-1 mt-2">
            <label className="block"><input type="radio" name="q3" /> Estabilidade</label>
            <label className="block"><input type="radio" name="q3" /> Retorno maior</label>
            <label className="block"><input type="radio" name="q3" /> Equilíbrio</label>
          </div>
        </div>
      </div>

      <button
        className="mt-8 bg-red-600 text-white px-6 py-2 rounded disabled:opacity-50"
        disabled={!stepComplete}
        onClick={() => navigate('/perfil')}
      >
        Ver meu perfil
      </button>
    </div>
  );
}

export default Questionnaire;
