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

  // Encontra a mesa selecionada para exibir o nome
  const mesaAtual = mesas.find(mesa => mesa.id === mesaSelecionada);

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
                    backgroundColor: mesa.ocupada ? "#2ecc71" : "#e74c3c",
                    color: "#fff",
                    border: "none",
                    padding: "8px 16px",
                    cursor: "pointer",
                    borderRadius: "20px",
                    fontSize: "12px",
                    fontWeight: "600",
                    textTransform: "uppercase",
                    letterSpacing: "0.5px",
                    boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
                    transition: "all 0.3s ease",
                    transform: "scale(1)"
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.backgroundColor = mesa.ocupada ? "#27ae60" : "#c0392b";
                    e.target.style.transform = "scale(1.05)";
                    e.target.style.boxShadow = "0 4px 12px rgba(0,0,0,0.2)";
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.backgroundColor = mesa.ocupada ? "#2ecc71" : "#e74c3c";
                    e.target.style.transform = "scale(1)";
                    e.target.style.boxShadow = "0 2px 6px rgba(0,0,0,0.15)";
                  }}
                >
                  {mesa.ocupada ? "Liberar" : "Ocupar"}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Bloco dos Itens - Aparece apenas quando uma mesa é selecionada */}
        {mesaSelecionada && (
          <div className="form-container box" style={{ flex: 1, position: 'relative' }}>
            <button 
              onClick={() => {
                setMesaSelecionada(null);
                setSelecionados({});
                setMsg("");
              }}
              style={{
                position: 'absolute',
                top: '-10px',
                right: '-10px',
                backgroundColor: "#ff4757",
                color: "#fff",
                border: "none",
                width: "32px",
                height: "32px",
                cursor: "pointer",
                borderRadius: "50%",
                fontSize: "16px",
                fontWeight: "bold",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
                transition: "all 0.2s ease",
                transform: "scale(1)",
                zIndex: 10
              }}
              onMouseEnter={(e) => {
                e.target.style.backgroundColor = "#ff3742";
                e.target.style.transform = "scale(1.1)";
                e.target.style.boxShadow = "0 4px 12px rgba(0,0,0,0.3)";
              }}
              onMouseLeave={(e) => {
                e.target.style.backgroundColor = "#ff4757";
                e.target.style.transform = "scale(1)";
                e.target.style.boxShadow = "0 2px 8px rgba(0,0,0,0.2)";
              }}
            >
              ✕
            </button>
            <h2>Fazer Pedido - {mesaAtual?.label}</h2>
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
        )}
      </div>
    </div>
  );
}