import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Input from "../components/inputs/Input";
import AuthLayout from "../components/layouts/AuthLayout";
import { validateEmail } from "../utils/helper"
import api from "../api";

// Formulário de Login
export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Gerenciar o envio de formulário de login
  const handleLogin = async (e) => {
    e.preventDefault();

    if(!validateEmail(email)) {
      setError("Por favor, insira um endereço de email válido.");
      return;
    }

    if(!password) {
      setError("Por favor, insira sua senha");
      return;
    }

    setError("");

    // Chamada da API de Login
    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      const { access_token, role } = response.data;

      if (access_token) {
        // salva o token
        localStorage.setItem("token", access_token);

        // atualiza estado global/contexto se tiver
        // updateUser(response.data);

        // redireciona conforme o role
        if (role === "garcom") {
          navigate("/garcom");
        } else {
          navigate("/cozinha");
        } 
      }
    } catch (error) {
      if (error.response && error.response.data.message) {
        setError(error.response.data.message);
      } else {
        setError("Algo deu errado. Por favor, tente novamente.");
      }
    }
  }

  return (
      <div className='form-container box'>
        <div style={{alignSelf: 'center', fontSize: '24px', fontWeight: '700'}}>
          <span style={{color: '#ef4444'}}>Pizza</span>
          <span style={{color: 'white'}}>Ticket</span>
        </div>

        <p>
          Por favor, insira suas informações para logar.
        </p>

        <form onSubmit={handleLogin}>
          <label style={{ color: 'white', fontSize: '12px' }}>
            Endereço de Email:
            <Input
              value={email}
              onChange={({ target }) => setEmail(target.value)}
              placeholder="john@example.com"
              type="text"
            />
          </label>

          <label style={{ color: 'white', fontSize: '12px' }}>
            Senha:
            <Input 
              value={password}
              onChange={({ target }) => setPassword(target.value)}
              placeholder="Mínimo 8 caracteres"
              type="password"
            />
          </label>

          {error && <p className='text-error'>{error}</p>}

          <button type='submit' className='btn-primary'>
            LOGIN
          </button>

          <p className='text-bottom'>
            Não possui uma conta? {" "}
            <Link className='custom-link' to='/signup'>
              SignUp
            </Link>
          </p>
        </form>
      </div>
  );
}
