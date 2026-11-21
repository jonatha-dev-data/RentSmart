"""Entidades de domínio: os tipos de imóvel da R.M Imóveis.

Hierarquia de classes:

    Imovel (abstrata)
    ├── ImovelResidencial (abstrata)  -> quartos + vaga de garagem
    │   ├── Apartamento               -> desconto de 5% sem crianças
    │   └── Casa
    └── Estudio                       -> pacote de estacionamento próprio

Cada classe conhece as próprias regras de preço (polimorfismo): quem usa um
``Imovel`` não precisa saber qual é o tipo concreto para calcular o aluguel.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

from dinheiro import dinheiro


@dataclass(frozen=True)
class ItemValor:
    """Uma linha do orçamento: descrição + valor em reais."""

    descricao: str
    valor: Decimal


class Imovel(ABC):
    """Classe base de qualquer imóvel locável."""

    NOME: str = ""
    ALUGUEL_BASE: Decimal = Decimal("0")

    @property
    def aluguel_base(self) -> Decimal:
        return dinheiro(self.ALUGUEL_BASE)

    @abstractmethod
    def descricao(self) -> str:
        """Texto curto que identifica o imóvel escolhido."""

    @abstractmethod
    def adicionais(self) -> list[ItemValor]:
        """Itens que se somam ao aluguel-base (quartos extras, vagas...)."""

    def percentual_desconto(self) -> Decimal:
        """Percentual de desconto aplicável (padrão: nenhum)."""
        return Decimal("0")

    def motivo_desconto(self) -> str:
        """Texto explicando o desconto aplicado."""
        return ""

    def subtotal_aluguel(self) -> Decimal:
        """Aluguel-base + adicionais, ainda sem desconto."""
        total = self.aluguel_base + sum((i.valor for i in self.adicionais()), Decimal("0"))
        return dinheiro(total)


class ImovelResidencial(Imovel, ABC):
    """Regras comuns a casas e apartamentos: quartos e vaga de garagem."""

    QUARTOS_PERMITIDOS = (1, 2)
    VALOR_GARAGEM = Decimal("300.00")
    ADICIONAL_SEGUNDO_QUARTO: Decimal = Decimal("0")

    def __init__(self, quartos: int, vaga_garagem: bool):
        if quartos not in self.QUARTOS_PERMITIDOS:
            raise ValueError("A quantidade de quartos deve ser 1 ou 2.")
        self.quartos = quartos
        self.vaga_garagem = bool(vaga_garagem)

    def descricao(self) -> str:
        plural = "quarto" if self.quartos == 1 else "quartos"
        return f"{self.NOME} de {self.quartos} {plural}"

    def adicionais(self) -> list[ItemValor]:
        itens = []
        if self.quartos == 2:
            itens.append(ItemValor("Adicional de segundo quarto", dinheiro(self.ADICIONAL_SEGUNDO_QUARTO)))
        if self.vaga_garagem:
            itens.append(ItemValor("Vaga de garagem", dinheiro(self.VALOR_GARAGEM)))
        return itens


class Apartamento(ImovelResidencial):
    NOME = "Apartamento"
    ALUGUEL_BASE = Decimal("700.00")
    ADICIONAL_SEGUNDO_QUARTO = Decimal("200.00")
    DESCONTO_SEM_CRIANCAS = Decimal("5")  # em %

    def __init__(self, quartos: int, vaga_garagem: bool, possui_criancas: bool):
        super().__init__(quartos, vaga_garagem)
        self.possui_criancas = bool(possui_criancas)

    def percentual_desconto(self) -> Decimal:
        # O desconto incide sobre o aluguel já com os adicionais.
        return Decimal("0") if self.possui_criancas else self.DESCONTO_SEM_CRIANCAS

    def motivo_desconto(self) -> str:
        if self.possui_criancas:
            return ""
        return f"Desconto de {self.DESCONTO_SEM_CRIANCAS}% (cliente sem crianças)"


class Casa(ImovelResidencial):
    NOME = "Casa"
    ALUGUEL_BASE = Decimal("900.00")
    ADICIONAL_SEGUNDO_QUARTO = Decimal("250.00")


class Estudio(Imovel):
    NOME = "Estúdio"
    ALUGUEL_BASE = Decimal("1200.00")
    VAGAS_DO_PACOTE = 2
    VALOR_PACOTE = Decimal("250.00")
    VALOR_VAGA_ADICIONAL = Decimal("60.00")

    def __init__(self, vagas: int = 0):
        """``vagas`` = total de vagas desejadas (0 = sem estacionamento).

        O estacionamento do estúdio é contratado em pacote de 2 vagas; por isso
        a quantidade total só pode ser 0 ou maior/igual a 2.
        """
        if vagas < 0 or vagas == 1:
            raise ValueError(
                f"Estúdio: informe 0 (sem vaga) ou no mínimo {self.VAGAS_DO_PACOTE} vagas (pacote inicial)."
            )
        self.vagas = vagas

    def descricao(self) -> str:
        return self.NOME

    def adicionais(self) -> list[ItemValor]:
        itens = []
        if self.vagas >= self.VAGAS_DO_PACOTE:
            itens.append(
                ItemValor(f"Pacote de estacionamento ({self.VAGAS_DO_PACOTE} vagas)", dinheiro(self.VALOR_PACOTE))
            )
            extras = self.vagas - self.VAGAS_DO_PACOTE
            if extras > 0:
                rotulo = "vaga adicional" if extras == 1 else "vagas adicionais"
                itens.append(
                    ItemValor(
                        f"{extras} {rotulo} (R$ 60,00 cada)",
                        dinheiro(self.VALOR_VAGA_ADICIONAL * extras),
                    )
                )
        return itens
