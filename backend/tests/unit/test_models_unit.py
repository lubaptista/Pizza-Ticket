from models import Usuario, Mesa

def test_usuario_model():
    u = Usuario(nome="Teste", email="t@t.com", password="123", role="admin")
    assert u.email == "t@t.com"

def test_mesa_model():
    m = Mesa(label="Mesa Teste")
    assert m.ocupada is False
