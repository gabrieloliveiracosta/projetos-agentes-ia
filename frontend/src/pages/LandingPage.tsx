
import { useNavigate } from 'react-router-dom';

function LandingPage() {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col items-center justify-center h-screen px-4 text-center">
      <h1 className="text-4xl font-bold text-red-600 mb-4">selfIA</h1>
      <p className="max-w-xl text-gray-700">
        Este é um protótipo de demonstração. Versão limitada para mostrar como nosso
        assessor inteligente monta carteiras de investimento personalizadas.
      </p>
      <button
        className="mt-10 bg-red-600 text-white px-6 py-3 rounded hover:bg-red-700 transition"
        onClick={() => navigate('/questionario')}
      >
        Continuar
      </button>
    </div>
  );
}

export default LandingPage;
