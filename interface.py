"""Interação com o usuário: leitura validada de dados e exibição do orçamento."""

from dinheiro import formatar_brl
from orcamento import Orcamento

LARGURA = 60


class EntradaUsuario:
    """Leitura de dados pelo terminal, repetindo a pergunta até a resposta ser válida."""

    @staticmethod
    def texto(pergunta: str) -> str:
        while True:
            resposta = input(pergunta).strip()
            if resposta:
                return resposta
            print("  Entrada inválida: o campo não pode ficar vazio.")

    @staticmethod
    def inteiro(pergunta: str, minimo: int, maximo: int | None = None) -> int:
        while True:
            resposta = input(pergunta).strip()
            try:
                numero = int(resposta)
            except ValueError:
                print("  Entrada inválida: digite um número inteiro.")
                continue
            if numero < minimo or (maximo is not None and numero > maximo):
                limite = f"entre {minimo} e {maximo}" if maximo is not None else f"maior ou igual a {minimo}"
                print(f"  Valor inválido: informe um número {limite}.")
                continue
            return numero

    @staticmethod
    def opcao(titulo: str, opcoes: list[str]) -> int:
        """Mostra um menu numerado e devolve o número escolhido (1..n)."""
        print(f"\n{titulo}")
        for i, texto in enumerate(opcoes, start=1):
            print(f"  {i} - {texto}")
        return EntradaUsuario.inteiro("Escolha uma opção: ", 1, len(opcoes))

    @staticmethod
    def sim_nao(pergunta: str) -> bool:
        while True:
            resposta = input(f"{pergunta} (s/n): ").strip().lower()
            if resposta in ("s", "sim"):
                return True
            if resposta in ("n", "nao", "não"):
                return False
            print("  Entrada inválida: responda com 's' ou 'n'.")


class ApresentadorOrcamento:
    """Monta o texto do resumo detalhado do orçamento."""

    @staticmethod
    def _linha(descricao: str, valor: str) -> str:
        pontos = "." * max(2, LARGURA - len(descricao) - len(valor) - 2)
        return f"  {descricao} {pontos} {valor}"

    def resumo(self, orc: Orcamento) -> str:
        linhas = [
            "=" * LARGURA,
            "R.M IMÓVEIS - ORÇAMENTO DE LOCAÇÃO (RentSmart)".center(LARGURA),
            "=" * LARGURA,
            f"Cliente: {orc.cliente}",
            f"Imóvel : {orc.imovel.descricao()}",
            "",
            "ALUGUEL MENSAL",
            self._linha("Aluguel-base", formatar_brl(orc.aluguel_base)),
        ]
        for item in orc.adicionais:
            linhas.append(self._linha(f"+ {item.descricao}", formatar_brl(item.valor)))
        linhas.append(self._linha("Subtotal", formatar_brl(orc.subtotal_aluguel)))
        if orc.percentual_desconto > 0:
            linhas.append(self._linha(f"- {orc.imovel.motivo_desconto()}", formatar_brl(orc.valor_desconto)))
        linhas.append(self._linha("VALOR MENSAL DO ALUGUEL", formatar_brl(orc.aluguel_mensal)))

        parcelas = orc.taxa.valores_parcelas()
        linhas += [
            "",
            "TAXA CONTRATUAL (cobrada à parte do aluguel)",
            self._linha("Valor total da taxa", formatar_brl(orc.taxa.valor)),
        ]
        if orc.taxa.parcelas == 1:
            linhas.append("  Condição: à vista (1 parcela).")
        else:
            linhas.append(f"  Condição: {orc.taxa.parcelas} parcelas")
            for numero, valor in enumerate(parcelas, start=1):
                linhas.append(self._linha(f"Parcela {numero}/{orc.taxa.parcelas} (mês {numero})", formatar_brl(valor)))

        linhas += [
            "",
            "PROJEÇÃO DO PRIMEIRO ANO (12 meses)",
            self._linha("Total de aluguéis", formatar_brl(orc.total_alugueis_12_meses)),
            self._linha("Total da taxa contratual", formatar_brl(orc.taxa.valor)),
            self._linha("TOTAL GERAL NO ANO", formatar_brl(orc.total_geral_12_meses)),
            "=" * LARGURA,
        ]
        return "\n".join(linhas)
