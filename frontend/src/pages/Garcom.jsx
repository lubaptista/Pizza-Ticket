import { useEffect, useState } from "react";
import api from "../api";

export default function Garcom() {
  const [mesas, setMesas] = useState([]);
  const [itens, setItens] = useState([]);
  const [selecionados, setSelecionados] = useState({}); // {itemId: quantidade}
  const [mesaSelecionada, setMesaSelecionada] = useState(null);
  const [pedidosAtuais, setPedidosAtuais] = useState(null); // guarda o pedido carregado da mesa
  const [modo, setModo] = useState("visualizar"); // visualizar | novoPedido
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
      setPedidosAtuais(null);
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

  // Buscar pedidos da mesa ao selecionar
  const selecionarMesa = async (mesaId) => {
    setMesaSelecionada(mesaId);
    setModo("visualizar");
    setPedidosAtuais(null);

    try {
      const res = await api.get(`/pedidos/mesa/${mesaId}`);
      if (res.data.length > 0) {
        setPedidosAtuais(res.data);
      } else {
        setPedidosAtuais(null);
      }
    } catch (err) {
      console.error(err);
      setMsg("Erro ao buscar pedidos da mesa");
    }
  };

  const finalizarMesa = async () => {
    if (!mesaSelecionada) return;
    try {
      await api.delete(`/pedidos/mesa/${mesaSelecionada}/finalizar`);
      setMsg("Mesa finalizada!");
      setMesaSelecionada(null);
      setPedidosAtuais(null);
      fetchMesas();
    } catch (err) {
      console.error(err);
      setMsg("Erro ao finalizar mesa");
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
                  onClick={() => selecionarMesa(mesa.id)}
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
                    padding: "6px 12px",
                    width: "50%",
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
        
        {/* Detalhes da mesa */}
        {mesaSelecionada && (
          <div className="form-container box" style={{ flex: 1 }}>
            <h2 style={{marginBottom: "10px"}}>{mesaAtual?.label}</h2>
            {/* Se existe pedido */}
            {pedidosAtuais?.length > 0 && modo === "visualizar" && (
              <>
              {pedidosAtuais.map((pedidoAtual) => {
              const total = pedidoAtual.itens.reduce(
                (acc, item) => acc + item.quantidade * item.preco,
                0
              );

              return (
                <div 
                  key={pedidoAtual.id} 
                  style={{
                    border: "1px solid #ddd",
                    borderRadius: "12px",
                    padding: "12px",
                    marginBottom: "16px",
                    boxShadow: "0 2px 6px rgba(0,0,0,0.1)",
                  }}
                >
                  <h3 style={{ marginBottom: "10px" }}>Pedido #{pedidoAtual.id}</h3>
                  <ul style={{ paddingLeft: "18px", marginBottom: "10px" }}>
                    {pedidoAtual.itens.map((item, idx) => (
                      <li key={idx} style={{ marginBottom: "4px" }}>
                        <b>{item.quantidade}x</b> {item.nome}  
                        — R${(item.preco * item.quantidade).toFixed(2)}
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}

              <div>
                <p>
                  <b>Total:</b> R${pedidosAtuais.total}
                </p>
                <div style={{display: "flex", gap: "5px"}}>
                  <button onClick={finalizarMesa} style={{ backgroundColor: "#e74c3c", color: "#fff" }}>
                    Finalizar Mesa
                  </button>
                  <button onClick={() => setModo("novoPedido")}>Adicionar Pedido</button>
                </div>
              </div>
              </>
            )}

            {/* Se não existe pedido */}
            {!pedidosAtuais && modo === "visualizar" && (
              <div>
                <p>Não há pedidos cadastrados.</p>
                <button onClick={() => setModo("novoPedido")}>Adicionar Pedido</button>
                <button onClick={finalizarMesa} style={{ backgroundColor: "#e74c3c", color: "#fff" }}>
                  Finalizar Mesa
                </button>
              </div>
            )} 

            {/* Bloco dos Itens - Aparece apenas quando uma mesa é selecionada */}
            {modo === "novoPedido" && (
              <div className="form-container box" style={{ flex: 1, position: 'relative' }}>
                <button 
                  onClick={() => {
                    setModo("visualizar")
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
                <h3 style={{marginBottom:'8px'}}>Adicionar Pedido</h3>
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
        )}
      </div>
    </div>
  );
}