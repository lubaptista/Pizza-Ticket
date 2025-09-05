// Visualizar Cardápio - Adicionar/editar categorias e itens
import { useEffect, useState } from "react";

export default function Cardapio() {
  const [itens, setItens] = useState([]);

  useEffect(() => {
    // Função para buscar os itens do backend
    async function fetchItens() {
      try {
        const response = await fetch("http://localhost:5000/cardapio/");
        if (!response.ok) throw new Error("Erro ao buscar itens do cardápio");
        const data = await response.json();
        setItens(data);
      } catch (error) {
        console.error(error);
      }
    }

    fetchItens();
  }, []);

  return (
     <div className="page">
      <h1>Cardápio</h1>
        {itens.length === 0 ? (
        <p>Carregando itens...</p>
      ) : (
        <div className="cardapio-grid">
          {itens.map((item) => (
            <div
              key={item.id}
              className="cardapio-card"
            >
              <h2>{item.nome}</h2>
              <p>Categoria: {item.categoria}</p>
              <p className="preco">R$ {item.preco.toFixed(2)}</p>
            </div>
          ))}
        </div>
      )}

    </div>
  );
}

