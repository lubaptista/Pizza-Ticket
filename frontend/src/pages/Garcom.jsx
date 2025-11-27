import { useEffect, useState } from "react";
import api from "../api";

export default function Garcom() {
  const [mesas, setMesas] = useState([]);
  const [itens, setItens] = useState([]);
  const [pedidos, setPedidos] = useState([]);
  const [selecionados, setSelecionados] = useState({});
  const [mesaSelecionada, setMesaSelecionada] = useState(null);
  const [blocoAtivo, setBlocoAtivo] = useState(null);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetchMesas();
    fetchItens();
    fetchPedidos();
  }, []);

  const fetchMesas = async () => {
    try {
      const res = await api.get("/pedidos/mesas");
      setMesas(res.data);
    } catch (err) {
      console.error(err);
      setMsg("Erro ao buscar mesas");
    }
  };

  const fetchItens = async () => {
    try {
      const res = await api.get("/itens/");
      setItens(res.data);
    } catch (err) {
      console.error(err);
      setMsg("Erro ao buscar itens");
    }
  };

  const fetchPedidos = async () => {
    try {
      const res = await api.get("/pedidos/todos");
      setPedidos(res.data);
    } catch (err) {
      console.error(err);
      setMsg("Erro ao buscar pedidos");
    }
  };

  const handleQuantidade = (itemId, quantidade) => {
    setSelecionados((prev) => ({ ...prev, [itemId]: quantidade }));
  };

  const selecionarMesa = (mesa) => {
    setMesaSelecionada(mesa.id);
    setSelecionados({});
    setMsg("");

    if (mesa.ocupada) {
      setBlocoAtivo(null);
    } else {
      setBlocoAtivo("ocupar");
    }
  };

  const ocuparMesa = async () => {
    if (!mesaSelecionada) return;
    try {
      await api.put(`/pedidos/mesa/${mesaSelecionada}/status`, { ocupada: true });
      setMsg("Mesa ocupada com sucesso!");
      fetchMesas();
      setBlocoAtivo(null);
    } catch (err) {
      console.error(err);
      setMsg("Erro ao ocupar mesa");
    }
  };

  const criarPedido = async () => {
  if (!mesaSelecionada) return setMsg("Selecione uma mesa!");
  const itensPedido = Object.entries(selecionados)
    .filter(([_id, quantidade]) => quantidade > 0)
    .map(([id, quantidade]) => ({
      id: parseInt(id),
      quantidade: parseInt(quantidade),
    }));

  if (itensPedido.length === 0) return setMsg("Selecione ao menos um item!");

  try {
    await api.post("/pedidos/criar", {
      mesa: mesaSelecionada,
      itens: itensPedido,
    });
    setMsg("Pedido criado!");
    setSelecionados({});
    await fetchMesas();
    await fetchPedidos();

    // Redireciona para visualizar os pedidos da mesa
    setBlocoAtivo("pedidos");
  } catch (err) {
    console.error(err);
    setMsg("Erro ao criar pedido");
  }
};


  const finalizarConta = async () => {
    if (!mesaSelecionada) return;

    try {
      // Libera a mesa
      await api.put(`/pedidos/mesa/${mesaSelecionada}/status`, { ocupada: false });
      // Remove todos os pedidos da mesa
      await api.delete(`/pedidos/mesa/${mesaSelecionada}/todos`);
      setMsg("Conta finalizada e pedidos removidos!");
      fetchMesas();
      fetchPedidos();
      setBlocoAtivo(null);
      setMesaSelecionada(null);
    } catch (err) {
      console.error(err);
      setMsg("Erro ao finalizar conta");
    }
  };

  const voltarParaMesas = () => {
    setBlocoAtivo(null);
    setMesaSelecionada(null);
    setSelecionados({});
    setMsg("");
  };

  const mesaAtual = mesas.find((m) => m.id === mesaSelecionada);

  const pedidosPorMesa =
    Array.isArray(pedidos) && pedidos.length > 0
      ? pedidos.reduce((acc, pedido) => {
          if (pedido && pedido.mesa) {
            if (!acc[pedido.mesa]) acc[pedido.mesa] = [];
            acc[pedido.mesa].push(pedido);
          }
          return acc;
        }, {})
      : {};

  return (
    <div className="page">
      <h1>Página do Garçom</h1>

      <div style={{ display: "flex", gap: "20px" }}>
        {/* Bloco Mesas */}
        <div className="form-container box" style={{ flex: 1 }}>
          <h2>Mesas</h2>
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            {mesas.length === 0 ? (
              <p>Carregando mesas...</p>
            ) : (
              mesas.map((mesa) => (
                <button
                  key={mesa.id}
                  onClick={() => selecionarMesa(mesa)}
                  style={{
                    padding: "10px",
                    cursor: "pointer",
                  }}
                >
                  {mesa.label} {mesa.ocupada ? "(ocupada)" : "(livre)"}
                </button>
              ))
            )}
          </div>
        </div>

        {/* Bloco Ações */}
        <div className="form-container box" style={{ flex: 2 }}>
          {!mesaSelecionada && (
            <div>
              <h2>Selecione uma mesa</h2>
              <p>Clique em uma mesa para ver as opções disponíveis.</p>
            </div>
          )}

          {mesaSelecionada && mesaAtual && !blocoAtivo && (
            <div>
              <h2>{mesaAtual.label}</h2>
              {mesaAtual.ocupada ? (
                <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginTop: "10px" }}>
                  <button onClick={() => setBlocoAtivo("finalizar")}>Finalizar Conta</button>
                  <button onClick={() => setBlocoAtivo("pedidos")}>Ver Pedidos</button>
                  <button onClick={() => setBlocoAtivo("fazer-pedido")}>Fazer Pedido</button>
                </div>
              ) : (
                <button onClick={() => setBlocoAtivo("ocupar")}>Ocupar Mesa</button>
              )}
              <button onClick={voltarParaMesas} style={{ marginTop: "20px" }}>
                Voltar
              </button>
            </div>
          )}

          {/* Bloco Ocupar Mesa */}
          {blocoAtivo === "ocupar" && (
            <div>
              <h2>Ocupar {mesaAtual?.label}</h2>
              <p>Confirma a ocupação desta mesa?</p>
              <div style={{ display: "flex", gap: "10px" }}>
                <button onClick={ocuparMesa}>Confirmar</button>
                <button onClick={() => setBlocoAtivo(null)}>Cancelar</button>
              </div>
            </div>
          )}

          {/* Bloco Fazer Pedido */}
          {blocoAtivo === "fazer-pedido" && (
            <div>
              <h2>Fazer Pedido - {mesaAtual?.label}</h2>
              <div className="cardapio-grid" style={{ gap: "0.75rem", padding: "0.5rem", marginTop: "5px" }}>
                {itens.map((item) => (
                  <div
                    key={item.id}
                    className="cardapio-card">
                    <div
                      style={{ display: "flex", alignItems: "center" }}
                    >
                      <span>{item.nome}ㅤ-ㅤ</span>
                      <span className="preco"> R${item.preco}</span>
                    </div>
                    <input
                      type="number"
                      min="0"
                      value={selecionados[item.id] || 0}
                      onChange={(e) => handleQuantidade(item.id, e.target.value)}
                      className="input-box"
                      style={{ marginTop: "6px", marginBottom: "0", padding: "6px" }}
                    />
                  </div>
                ))}
              </div>
              <div style={{ display: "flex", gap: "10px", marginTop: "10px" }}>
                <button className="btn-primary" onClick={criarPedido} style={{ flex: 1 }}>
                  Confirmar
                </button>
                <button className="btn-primary" onClick={() => setBlocoAtivo(null)} style={{ flex: 1 }}>
                  Voltar
                </button>
              </div>
            </div>
          )}

          {/* Bloco Ver Pedidos */}
          {blocoAtivo === "pedidos" && (
            <div>
              <h2>Pedidos - {mesaAtual?.label}</h2>
              {!pedidosPorMesa[`Mesa ${mesaSelecionada}`] ||
              pedidosPorMesa[`Mesa ${mesaSelecionada}`].length === 0 ? (
                <p>Nenhum pedido encontrado.</p>
              ) : (
                <>
                  {pedidosPorMesa[`Mesa ${mesaSelecionada}`].map((pedido) => (
                    <div
                      key={pedido.id}
                      style={{
                        border: "1px solid #ddd",
                        padding: "12px",
                        margin: "10px 0px",
                        borderRadius: "5px",
                      }}
                    >
                      <h4>Pedido #{pedido.id}</h4>
                      <p style={{ marginBottom: "15px" }}>
                        Status:{" "}
                        <span
                          style={{
                            color: pedido.status === "pronto" ? "#2e7d32" : "#1976d2",
                            fontWeight: "bold",
                          }}
                        >
                          {pedido.status}
                        </span>
                      </p>
                      {pedido.itens && pedido.itens.length > 0 && (
                        <div style={{ padding: "0px 12px" }}>
                          <ul>
                            {pedido.itens.map((item, i) => (
                              <li
                                key={i}
                                style={{
                                  color:
                                    item.status === "pronto"
                                      ? "#f8faf8ff"
                                      : "#fcfafaff",
                                }}
                              >
                                {item.quantidade}x {item.nome} - R$
                                {(item.preco * item.quantidade).toFixed(2)}
                                {item.status === "pronto" && <span> ✅</span>}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}

                  {/* cálculo do total da mesa */}
                  <div style={{ marginTop: "15px", fontWeight: "bold", fontSize: "16px" }}>
                    Total da Mesa: R$
                    {pedidosPorMesa[`Mesa ${mesaSelecionada}`]
                      .reduce((total, pedido) => {
                        return (
                          total +
                          pedido.itens.reduce(
                            (subTotal, item) =>
                              subTotal + item.quantidade * item.preco,
                            0
                          )
                        );
                      }, 0)
                      .toFixed(2)}
                  </div>
                </>
              )}
              <button onClick={() => setBlocoAtivo(null)} style={{ marginTop: "15px" }}>
                Voltar
              </button>
            </div>
          )}

          {/* Bloco Finalizar Conta */}
          {blocoAtivo === "finalizar" && (
            <div>
              <h2>Finalizar Conta - {mesaAtual?.label}</h2>
              <p>Confirma a finalização da conta e remoção dos pedidos?</p>
              <div style={{ display: "flex", gap: "10px" }}>
                <button onClick={finalizarConta} className="btn-primary" style={{ flex: 1 }}>
                  Confirmar
                </button>
                <button onClick={() => setBlocoAtivo(null)} className="btn-primary" style={{ flex: 1 }}>
                  Cancelar
                </button>
              </div>
            </div>
          )}

          {msg && (
            <div
              style={{
                marginTop: "20px",
                padding: "10px",
                backgroundColor: msg.includes("Erro") ? "#ffebee" : "#e8f5e8",
                color: msg.includes("Erro") ? "#c62828" : "#2e7d32",
                borderRadius: "5px",
              }}
            >
              {msg}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
