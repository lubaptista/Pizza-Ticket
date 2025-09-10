import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";

function Navbar() {
  const navigate = useNavigate();
  const role = localStorage.getItem("role");

  let homeRoute = "/";
  if (role === "garcom") {
    homeRoute = "/garcom";
  } else if (role === "cozinha") {
    homeRoute = "/cozinha";
  } else {
    homeRoute = "/admin";
  }

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/"); // volta para login
  };

  return (
    <nav className="navbar">
      {/* Logo */}
      <Link to={homeRoute}>
        <span style={{color: '#ef4444'}}>Pizza</span>
        <span style={{color: 'white'}}>Ticket</span>
      </Link>

      {/* Links */}
      <div className="navbar-links-container">
        <Link to="/nova-categoria">
          Nova categoria
        </Link>
        <Link to="/cardapio">
          Cardápio
        </Link>

        {/* Logout */}
        <button onClick={handleLogout}>
          <LogOut size={20} />
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
