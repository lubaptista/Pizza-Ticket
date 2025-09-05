import React from "react";
import { Link } from "react-router-dom";
import { LogOut } from "lucide-react";

function Navbar() {
  return (
    <nav className="navbar">
      {/* Logo */}
      <Link to="/">
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
        <button>
          <LogOut size={20} />
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
