import { Routes, Route, Link } from "react-router-dom";
import Login from "./pages/Login";
import Garcom from "./pages/Garcom";
import Cozinha from "./pages/Cozinha";
import Cardapio from "./pages/Cardapio";
import Pedidos from "./pages/Pedidos";

export default function App() {
  return (
    <div>
      {/* <nav>
        <Link to="/">Login</Link> |{" "}
        <Link to="/garcom">Garçom</Link> |{" "}
        <Link to="/cozinha">Cozinha</Link> |{" "}
        <Link to="/cardapio">Cardápio</Link> |{" "}
        <Link to="/pedidos">Pedidos</Link>
      </nav> */}
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/garcom" element={<Garcom />} />
        <Route path="/cozinha" element={<Cozinha />} />
        <Route path="/cardapio" element={<Cardapio />} />
        <Route path="/pedidos" element={<Pedidos />} />
      </Routes>
    </div>
  );
}
