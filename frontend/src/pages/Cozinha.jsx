import { useEffect, useState } from "react";
import api from "../api";

export default function Cozinha() {
  const [pedidos, setPedidos] = useState([]);
  const [msg, setMsg] = useState("");
  const [mesaSelecionada, setMesaSelecionada] = useState(null);

  // Carrega pedidos abertos
  const fetchPedidos = async () => {
    try {
      const res = await api.get("/pedidos/");
      // inicializa status local dos itens
      const pedidosComStatusLocal = res.data.map(pedido => ({
        ...pedido,
        itens: pedido.itens.map(item => ({ ...item, statusLocal: item.status }))
      }));
      setPedidos(pedidosComStatusLocal);
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

  // Marca item como pronto localmente
  const marcarItemProntoLocal = (pedidoId, itemId) => {
    setPedidos(prev =>
      prev.map(pedido =>
        pedido.id === pedidoId
          ? {
              ...pedido,
              itens: pedido.itens.map(item =>
                item.id === itemId ? { ...item, statusLocal: 'pronto' } : item
              )
            }
          : pedido
      )
    );
  };

  // Atualiza pedido completo no servidor e remove da tela
  const finalizarPedido = async (pedidoId) => {
    try {
      await api.patch(`/pedidos/${pedidoId}/status`, { status: 'pronto' });
      setPedidos(prev => prev.filter(pedido => pedido.id !== pedidoId));
      setMsg("✅ Pedido concluído!");
    } catch (err) {
      console.error(err);
      setMsg("❌ Erro ao finalizar pedido");
    }
  };

  // Agrupa pedidos por mesa
  const pedidosPorMesa = pedidos.reduce((acc, pedido) => {
    if (!acc[pedido.mesa]) acc[pedido.mesa] = []; 
    acc[pedido.mesa].push(pedido);
    return acc;
  }, {});

  return (
    <div className="page" style={{ display: 'flex', gap: '20px' }}>
      {/* Bloco das Mesas */}
      <div className="form-container box" style={{ width: '200px', flexShrink: 0, padding: '1rem' }}>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '12px' }}>Mesas</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {Object.keys(pedidosPorMesa).map((mesa) => (
            <button
              key={mesa}
              onClick={() => setMesaSelecionada(mesa)}
              style={{
                padding: "10px 16px",
                textAlign: "left",
                borderRadius: "10px",
                border: mesaSelecionada === mesa ? "2px solid #1368EC" : "none",
                backgroundColor: mesaSelecionada === mesa ? "#1368EC" : "#1f2937",
                color: "white",
                cursor: "pointer",
                fontWeight: mesaSelecionada === mesa ? "600" : "500",
                transition: "all 0.3s ease",
                boxShadow: "0 3px 8px rgba(0,0,0,0.2)",
                fontSize: "0.9rem"
              }}
              onMouseEnter={(e) => {
                if (mesaSelecionada !== mesa) e.target.style.backgroundColor = "#2e3a59";
                e.target.style.transform = "scale(1.02)";
                e.target.style.boxShadow = "0 5px 12px rgba(0,0,0,0.25)";
              }}
              onMouseLeave={(e) => {
                if (mesaSelecionada !== mesa) e.target.style.backgroundColor = "#1f2937";
                e.target.style.transform = "scale(1)";
                e.target.style.boxShadow = "0 3px 8px rgba(0,0,0,0.2)";
              }}
            >
            {mesa}
            </button>
          ))}
        </div>
      </div>

      {/* Bloco de Pedidos */}
      {mesaSelecionada && (
        <div className="form-container box" style={{ flex: 1, position: 'relative', padding: '1rem' }}>
          <button
            onClick={() => setMesaSelecionada(null)}
            style={{
              position: 'absolute',
              top: '-8px',
              right: '-8px',
              backgroundColor: "#ff4757",
              color: "#fff",
              border: "none",
              width: "28px",
              height: "28px",
              cursor: "pointer",
              borderRadius: "50%",
              fontSize: "14px",
              fontWeight: "bold",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
              transition: "all 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "#ff3742";
              e.target.style.transform = "scale(1.1)";
              e.target.style.boxShadow = "0 4px 12px rgba(0,0,0,0.3)";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "#ff4757";
              e.target.style.transform = "scale(1)";
              e.target.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
            }}
          >
            ✕
          </button>

          <h2 style={{ fontSize: '1.2rem', marginBottom: '10px' }}>Pedidos - Mesa {mesaSelecionada}</h2>

          {pedidosPorMesa[mesaSelecionada]?.map((pedido) => {
            const todosProntos = pedido.itens.every(item => item.statusLocal === 'pronto');

            return (
              <div key={pedido.id} className="cardapio-card" style={{ marginBottom: '10px', padding: '12px' }}>
                <h3 style={{ fontSize: '1rem', marginBottom: '6px' }}>Pedido #{pedido.id}</h3>
                {pedido.itens.map((item) => (
                  <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', marginTop: '6px', fontSize: '0.9rem' }}>
                    <span>{item.nome} x{item.quantidade}</span>
                    {item.statusLocal !== 'pronto' && (
                      <button
                        onClick={() => marcarItemProntoLocal(pedido.id, item.id)}
                        style={{
                          padding: '3px 8px',
                          backgroundColor: '#4ade80',
                          color: 'black',
                          border: 'none',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          fontWeight: '600',
                          fontSize: '0.8rem'
                        }}
                      >
                        ✅ Pronto
                      </button>
                    )}
                  </div>
                ))}
                {todosProntos && (
                  <button
                    onClick={() => finalizarPedido(pedido.id)}
                    style={{
                      marginTop: '8px',
                      width: '100%',
                      padding: '6px',
                      backgroundColor: '#1368EC',
                      color: 'white',
                      border: 'none',
                      borderRadius: '8px',
                      fontWeight: '600',
                      cursor: 'pointer'
                    }}
                  >
                    🎉 Pedido Pronto
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}

      {msg && <div style={{ position: 'fixed', bottom: '20px', right: '20px', color: msg.includes('❌') ? '#ef4444' : '#4ade80' }}>{msg}</div>}
    </div>
  );
}
