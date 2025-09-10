import { useEffect, useState } from "react";
import api from "../api";

export default function Cozinha() {
  const [pedidos, setPedidos] = useState([]);
  const [msg, setMsg] = useState("");

  // Carrega pedidos abertos
  const fetchPedidos = async () => {
    try {
      const res = await api.get("/pedidos/");
      setPedidos(res.data);
    } catch (err) {
      console.error(err);
      if (err.code === "ERR_NETWORK") {
        setMsg("❌ Erro de conexão com o servidor.");
      }
    }
  };

  useEffect(() => {
    fetchPedidos();
  }, []);

  // Atualiza status de um item
  const atualizarStatusItem = async (pedidoId, itemId, novoStatus) => {
    try {
      await api.patch(`/pedidos/item/${itemId}/status`, {
        status: novoStatus,
      });
      setMsg("✅ Status atualizado!");
      fetchPedidos(); // recarrega os pedidos
    } catch (err) {
      console.error(err);
      setMsg("❌ Erro ao atualizar status");
    }
  };

  return (
    <div className="page">
      <h1> Página da Cozinha</h1>

      <div className="form-container box">
        {pedidos.length === 0 ? (
          <div className="empty-state">
            <p>📝 Nenhum pedido em aberto.</p>
          </div>
        ) : (
          <div className="pedidos-grid">
            {pedidos.map((pedido) => (
              <div key={pedido.id} className="pedido-card">
                <div className="pedido-header">
                  <h2> {pedido.mesa}</h2>
                  <span className="pedido-id">Pedido #{pedido.id}</span>
                </div>
                
                <div className="itens-container">
                  {pedido.itens && pedido.itens.length > 0 ? (
                    pedido.itens.map((item, index) => (
                      <div 
                        key={item.id || index} 
                        className={`item-card ${item.status || 'pendente'}`}
                      >
                        <div className="item-info">
                          <span className="item-nome">{item.nome || 'Item sem nome'}</span>
                          <span className="item-quantidade">x{item.quantidade || 1}</span>
                        </div>
                        
                        <div className="item-status">
                          <span className={`status-badge ${item.status || 'pendente'}`}>
                            {item.status === 'pronto' ? '✅' : '⏳'} 
                            {item.status || 'Pendente'}
                          </span>
                        </div>
                        
                        {item.status !== "pronto" && (
                          <button
                            onClick={() =>
                              atualizarStatusItem(pedido.id, item.id, "pronto")
                            }
                            className="btn-pronto"
                          >
                            ✅ Marcar como pronto
                          </button>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="no-items">
                      <p>⚠️ Nenhum item encontrado neste pedido</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {msg && (
          <div className={`message ${msg.includes("✅") ? "success" : "error"}`}>
            {msg} 
          </div>
        )}
      </div>
    </div>
  );
}
