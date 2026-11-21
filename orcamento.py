"""Regras de orçamento: taxa contratual, valor mensal e projeção de 12 meses."""

from dataclasses import dataclass
from decimal import Decimal

from dinheiro import dinheiro
from imoveis import Imovel, ItemValor


class TaxaContratual:
    """Taxa única de contrato, parcelável em até 5 vezes.

    É tratada separadamente do aluguel: não entra no valor mensal da locação,
    apenas na projeção de pagamentos (parcela a parcela).
    """

    VALOR_PADRAO = Decimal("2000.00")
    MAX_PARCELAS = 5

    def __init__(self, parcelas: int, valor: Decimal = VALOR_PADRAO):
        if not 1 <= parcelas <= self.MAX_PARCELAS:
            raise ValueError(f"O parcelamento deve ser de 1 a {self.MAX_PARCELAS} vezes.")
        self.valor = dinheiro(valor)
        self.parcelas = parcelas

    def valores_parcelas(self) -> list[Decimal]:
        """Divide a taxa em parcelas; sobras de centavos vão para as primeiras.

        Garante que a soma das parcelas seja exatamente o valor da taxa.
        """
        total_centavos = int(self.valor * 100)
        base, resto = divmod(total_centavos, self.parcelas)
        return [Decimal(base + (1 if i < resto else 0)) / 100 for i in range(self.parcelas)]


@dataclass(frozen=True)
class LinhaProjecao:
    """Um mês da projeção de pagamentos."""

    mes: int
    aluguel: Decimal
    parcela_taxa: Decimal

    @property
    def total_mes(self) -> Decimal:
        return dinheiro(self.aluguel + self.parcela_taxa)


class Orcamento:
    """Une o imóvel escolhido e a taxa contratual e calcula todos os valores."""

    MESES_CONTRATO = 12

    def __init__(self, cliente: str, imovel: Imovel, taxa: TaxaContratual):
        self.cliente = cliente
        self.imovel = imovel
        self.taxa = taxa

    # --- aluguel mensal -------------------------------------------------
    @property
    def aluguel_base(self) -> Decimal:
        return self.imovel.aluguel_base

    @property
    def adicionais(self) -> list[ItemValor]:
        return self.imovel.adicionais()

    @property
    def subtotal_aluguel(self) -> Decimal:
        return self.imovel.subtotal_aluguel()

    @property
    def percentual_desconto(self) -> Decimal:
        return self.imovel.percentual_desconto()

    @property
    def valor_desconto(self) -> Decimal:
        return dinheiro(self.subtotal_aluguel * self.percentual_desconto / 100)

    @property
    def aluguel_mensal(self) -> Decimal:
        return dinheiro(self.subtotal_aluguel - self.valor_desconto)

    # --- projeção -------------------------------------------------------
    def projecao(self) -> list[LinhaProjecao]:
        """Projeção dos 12 meses: aluguel fixo + parcelas da taxa nos primeiros meses."""
        parcelas = self.taxa.valores_parcelas()
        linhas = []
        for mes in range(1, self.MESES_CONTRATO + 1):
            parcela = parcelas[mes - 1] if mes <= len(parcelas) else Decimal("0.00")
            linhas.append(LinhaProjecao(mes, self.aluguel_mensal, dinheiro(parcela)))
        return linhas

    @property
    def total_alugueis_12_meses(self) -> Decimal:
        return dinheiro(sum((l.aluguel for l in self.projecao()), Decimal("0")))

    @property
    def total_geral_12_meses(self) -> Decimal:
        return dinheiro(sum((l.total_mes for l in self.projecao()), Decimal("0")))
