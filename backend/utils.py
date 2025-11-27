# backend/utils.py
from datetime import datetime

# Função Dummy para ser testada unitariamente (1)
def valida_mesa_id(mesa_id: int) -> bool:
    """Verifica se o ID da mesa é um número positivo válido."""
    return isinstance(mesa_id, int) and mesa_id > 0

# Função Dummy para ser testada unitariamente (2)
def calcula_valor_total_pedido(itens: list) -> float:
    """Calcula o valor total do pedido com base nos itens e quantidades."""
    total = 0.0
    for item in itens:
        if item['preco'] < 0:
            raise ValueError("Preço não pode ser negativo")
        total += item['preco'] * item['quantidade']
    return round(total, 2)

# Função Dummy para ser testada unitariamente (3)
def formata_data_para_exibicao(data: datetime) -> str:
    """Formata um objeto datetime para um formato legível."""
    return data.strftime("%d/%m/%Y %H:%M:%S")

# Função Dummy para ser testada unitariamente (4)
def verifica_status_valido(status: str) -> bool:
    """Verifica se o status é um dos permitidos."""
    status_permitidos = ["aberto", "preparando", "finalizado", "cancelado"]
    return status.lower() in status_permitidos