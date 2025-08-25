import { useState } from "react";
import { Link } from "react-router-dom";
import Input from "../components/inputs/Input";
import AuthLayout from "../components/layouts/AuthLayout";
import { validateEmail } from "../utils/helper"
import api from "../api";

// Formulário de Login
export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

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

      const { token, role } = response.data;

      if (token) {
        // salva o token
        localStorage.setItem("token", token);

        // atualiza estado global/contexto se tiver
        updateUser(response.data);

        // redireciona conforme o role
        if (role === "admin") {
          navigate("/admin/dashboard");
        } else {
          navigate("/user/dashboard");
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
    <AuthLayout>
      <div className='box'>
        <h3>Bem-vindo de volta!</h3>
        <p>
          Por favor, insira suas informações para logar.
        </p>

        <form onSubmit={handleLogin}>
          <Input 
            value={email}
            onChange={({ target }) => setEmail(target.value)}
            label="Endereço de Email"
            placeholder="john@example.com"
            type="text"
          />

          <Input 
            value={password}
            onChange={({ target }) => setPassword(target.value)}
            label="Senha"
            placeholder="Mínimo 8 caracteres"
            type="password"
          />

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
    </AuthLayout>
  );
}
