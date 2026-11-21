"""Geração do arquivo CSV com a projeção de 12 meses."""

import csv

from dinheiro import formatar_csv
from orcamento import Orcamento


class ExportadorCSV:
    """Grava a projeção em CSV compatível com o Excel em português.

    Separador ``;``, vírgula decimal e codificação UTF-8 com BOM (acentos
    corretos ao abrir direto no Excel).
    """

    CABECALHO = ["mes", "aluguel_mensal", "parcela_taxa_contratual", "total_do_mes"]

    def __init__(self, caminho: str = "projecao_locacao_12_meses.csv"):
        self.caminho = caminho

    def exportar(self, orcamento: Orcamento) -> str:
        with open(self.caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(self.CABECALHO)
            for linha in orcamento.projecao():
                escritor.writerow(
                    [
                        linha.mes,
                        formatar_csv(linha.aluguel),
                        formatar_csv(linha.parcela_taxa),
                        formatar_csv(linha.total_mes),
                    ]
                )
        return self.caminho
