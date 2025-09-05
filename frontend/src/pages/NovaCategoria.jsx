import React, { useState } from "react";
import Navbar from "../components/layouts/Navbar";

function NovaCategoria() {
  const [nome, setNome] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!nome.trim()) {
      alert("Digite o nome da categoria!");
      return;
    }
    console.log("Categoria cadastrada:", nome);
    setNome(""); // limpa o input depois
  }

  return (
    <form onSubmit={handleSubmit} className="form-container">
        <h1>
        Nova categoria
        </h1>

        <input
        type="text"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        placeholder="Digite o nome para categoria"
        />

        <button type="submit">
        Cadastrar
        </button>
    </form>
  );
}

export default NovaCategoria;
