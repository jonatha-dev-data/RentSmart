"""Utilitários para tratamento de valores monetários.

Todo valor em reais é manipulado como ``Decimal`` (nunca ``float``) para
evitar erros de arredondamento em cálculos financeiros.
"""

from decimal import Decimal, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


def dinheiro(valor) -> Decimal:
    """Converte um valor para Decimal com duas casas (arredondamento comercial)."""
    return Decimal(str(valor)).quantize(CENTAVO, rounding=ROUND_HALF_UP)


def formatar_brl(valor) -> str:
    """Formata um valor no padrão brasileiro. Ex.: 1234.5 -> 'R$ 1.234,50'."""
    texto = f"{dinheiro(valor):,.2f}"  # 1,234.50
    texto = texto.replace(",", "#").replace(".", ",").replace("#", ".")
    return f"R$ {texto}"


def formatar_csv(valor) -> str:
    """Formata um valor para o CSV (vírgula decimal, sem símbolo de moeda)."""
    return f"{dinheiro(valor):.2f}".replace(".", ",")
