import { Routes, Route, Link } from "react-router-dom";
import Login from "./pages/Login";
import Garcom from "./pages/Garcom";
import Cozinha from "./pages/Cozinha";
import Cardapio from "./pages/Cardapio";
import Pedidos from "./pages/Pedidos";
import NovaCategoria from "./pages/NovaCategoria";
import Layout from "./components/layouts/Layout";

export default function App() {
  return (
    <Routes>
      {/* <nav>
        <Link to="/">Login</Link> |{" "}
        <Link to="/garcom">Garçom</Link> |{" "}
        <Link to="/cozinha">Cozinha</Link> |{" "}
        <Link to="/cardapio">Cardápio</Link> |{" "}
        <Link to="/pedidos">Pedidos</Link>
      </nav> */}
        <Route  element={<Layout hideNavbar={true} />}>
          <Route path="/" element={<Login />} />
        </Route>

        <Route element={<Layout />}>
          <Route path="/garcom" element={<Garcom />} />
          <Route path="/cozinha" element={<Cozinha />} />
          <Route path="/cardapio" element={<Cardapio />} />
          <Route path="/nova-categoria" element={<NovaCategoria />} />
          <Route path="/pedidos" element={<Pedidos />} />
        </Route>
    </Routes>
  );
}
