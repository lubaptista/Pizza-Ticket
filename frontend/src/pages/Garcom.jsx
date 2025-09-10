import { useEffect, useState } from "react";
import api from "../api";

export default function Garcom() {
  const [mesas, setMesas] = useState([]);
  const [itens, setItens] = useState([]);
  const [selecionados, setSelecionados] = useState({}); // {itemId: quantidade}
  const [mesaSelecionada, setMesaSelecionada] = useState(null);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetchMesas();
    fetchItens();
  }, []);

  // Busca todas as mesas
  const fetchMesas = async () => {
    try {
      const res = await api.get("/pedidos/mesas");
      setMesas(res.data);
    } catch (err) {
      console.error(err);
      setMsg("Erro ao buscar mesas");
    }
  };

  // Busca todos os itens
  const fetchItens = async () => {
    try {
      const res = await api.get("/itens/");
      setItens(res.data);
    } catch (err) {
      console.error(err);
      setMsg("Erro ao buscar itens");
    }
  };

  // Atualiza quantidade de um item selecionado
  const handleQuantidade = (itemId, quantidade) => {
    setSelecionados((prev) => ({ ...prev, [itemId]: quantidade }));
  };

  // Cria um novo pedido
  const criarPedido = async () => {
    if (!mesaSelecionada) return setMsg("Selecione uma mesa!");
    const itensPedido = Object.entries(selecionados).map(([id, quantidade]) => ({
      id: parseInt(id),
      quantidade: parseInt(quantidade)
    }));
    if (itensPedido.length === 0) return setMsg("Selecione ao menos um item!");

    try {
      await api.post("/pedidos/criar", {
        mesa: mesaSelecionada,
        itens: itensPedido
      });
      setMsg("Pedido criado!");
      setSelecionados({});
      setMesaSelecionada(null);
      fetchMesas();
    } catch (err) {
      console.error(err);
      setMsg("Erro ao criar pedido");
    }
  };

  // Função para alterar status da mesa (ocupada/livre)
  const alterarStatusMesa = async (mesaId, ocupada) => {
    try {
      await api.put(`/pedidos/mesa/${mesaId}/status`, { ocupada });
      fetchMesas(); // Atualiza a lista de mesas
    } catch (err) {
      console.error(err);
      setMsg("Erro ao alterar status da mesa");
    }
  };

  return (
    <div className="page">
      <h1>Página do Garçom</h1>

      <div style={{ display: 'flex', gap: '20px' }}>
        {/* Bloco das Mesas */}
        <div className="form-container box" style={{ flex: 1 }}>
          <h2>Mesas</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {mesas.map((mesa) => (
              <div key={mesa.id} style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <button
                  onClick={() => setMesaSelecionada(mesa.id)}
                  style={{ fontWeight: mesa.id === mesaSelecionada ? "bold" : "normal" }}
                >
                  {mesa.label} {mesa.ocupada ? "(ocupada)" : "(livre)"}
                </button>
                <button
                  onClick={() => alterarStatusMesa(mesa.id, !mesa.ocupada)}
                  style={{
                    backgroundColor: mesa.ocupada ? "#4caf50" : "#f44336",
                    color: "#fff",
                    border: "none",
                    padding: "5px 10px",
                    cursor: "pointer"
                  }}
                >
                  {mesa.ocupada ? "Liberar" : "Ocupar"}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Bloco dos Itens */}
        <div className="form-container box" style={{ flex: 1 }}>
          <h2>Itens</h2>
          {itens.map((item) => (
            <div key={item.id}>
              <span>{item.nome} - R${item.preco}</span>
              <input
                type="number"
                min="0"
                value={selecionados[item.id] || 0}
                onChange={(e) => handleQuantidade(item.id, e.target.value)}
              />
            </div>
          ))}

          <button onClick={criarPedido}>Abrir Pedido</button>
          {msg && <p>{msg}</p>}
        </div>
      </div>
    </div>
  );
}
