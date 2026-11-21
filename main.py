"""RentSmart - Sistema de orçamento de locação da R.M Imóveis.

Execute com:  python main.py
"""

from exportador import ExportadorCSV
from imoveis import Apartamento, Casa, Estudio, Imovel
from interface import ApresentadorOrcamento, EntradaUsuario
from orcamento import Orcamento, TaxaContratual


class AplicacaoRentSmart:
    """Orquestra o fluxo: entrada -> objetos de domínio -> orçamento -> saídas."""

    def __init__(self):
        self.entrada = EntradaUsuario()
        self.apresentador = ApresentadorOrcamento()
        self.exportador = ExportadorCSV()

    # --- coleta de dados por tipo de imóvel ------------------------------
    def _coletar_apartamento(self) -> Imovel:
        quartos = self.entrada.inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = self.entrada.sim_nao("Deseja vaga de garagem?")
        criancas = self.entrada.sim_nao("O cliente possui crianças?")
        return Apartamento(quartos, garagem, criancas)

    def _coletar_casa(self) -> Imovel:
        quartos = self.entrada.inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = self.entrada.sim_nao("Deseja vaga de garagem?")
        return Casa(quartos, garagem)

    def _coletar_estudio(self) -> Imovel:
        vagas = 0
        if self.entrada.sim_nao("Deseja estacionamento? (pacote inicial de 2 vagas)"):
            vagas = self.entrada.inteiro("Total de vagas desejadas (mínimo 2): ", 2)
        return Estudio(vagas)

    def _coletar_imovel(self) -> Imovel:
        escolha = self.entrada.opcao("Tipo de imóvel:", ["Apartamento", "Casa", "Estúdio"])
        coletores = {1: self._coletar_apartamento, 2: self._coletar_casa, 3: self._coletar_estudio}
        return coletores[escolha]()

    # --- fluxo principal ---------------------------------------------------
    def executar(self) -> None:
        print("=" * 60)
        print("RentSmart - R.M Imóveis".center(60))
        print("=" * 60)

        cliente = self.entrada.texto("Nome do cliente: ")
        imovel = self._coletar_imovel()
        parcelas = self.entrada.inteiro("\nTaxa contratual de R$ 2.000,00 - parcelas (1 a 5): ", 1, 5)

        orcamento = Orcamento(cliente, imovel, TaxaContratual(parcelas))

        print()
        print(self.apresentador.resumo(orcamento))

        caminho = self.exportador.exportar(orcamento)
        print(f"\nProjeção dos 12 meses salva em: {caminho}")


if __name__ == "__main__":
    try:
        AplicacaoRentSmart().executar()
    except (KeyboardInterrupt, EOFError):
        print("\nOperação cancelada pelo usuário.")
