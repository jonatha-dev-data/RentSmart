"""Testes automatizados das regras de negócio.  Execute: python -m unittest -v"""

import unittest
from decimal import Decimal

from imoveis import Apartamento, Casa, Estudio
from orcamento import Orcamento, TaxaContratual

D = Decimal


def orcar(imovel, parcelas=5):
    return Orcamento("Teste", imovel, TaxaContratual(parcelas))


class TestApartamento(unittest.TestCase):
    def test_1_quarto_com_criancas_sem_garagem(self):
        self.assertEqual(orcar(Apartamento(1, False, True)).aluguel_mensal, D("700.00"))

    def test_1_quarto_sem_criancas_tem_5_por_cento(self):
        self.assertEqual(orcar(Apartamento(1, False, False)).aluguel_mensal, D("665.00"))

    def test_2_quartos_garagem_sem_criancas(self):
        # (700 + 200 + 300) = 1200 -> -5% = 1140
        o = orcar(Apartamento(2, True, False))
        self.assertEqual(o.subtotal_aluguel, D("1200.00"))
        self.assertEqual(o.valor_desconto, D("60.00"))
        self.assertEqual(o.aluguel_mensal, D("1140.00"))

    def test_2_quartos_com_criancas(self):
        self.assertEqual(orcar(Apartamento(2, False, True)).aluguel_mensal, D("900.00"))

    def test_quartos_invalidos(self):
        with self.assertRaises(ValueError):
            Apartamento(3, False, True)


class TestCasa(unittest.TestCase):
    def test_1_quarto(self):
        self.assertEqual(orcar(Casa(1, False)).aluguel_mensal, D("900.00"))

    def test_2_quartos_com_garagem(self):
        self.assertEqual(orcar(Casa(2, True)).aluguel_mensal, D("1450.00"))

    def test_casa_nunca_tem_desconto(self):
        self.assertEqual(orcar(Casa(1, False)).valor_desconto, D("0.00"))


class TestEstudio(unittest.TestCase):
    def test_sem_estacionamento(self):
        self.assertEqual(orcar(Estudio(0)).aluguel_mensal, D("1200.00"))

    def test_pacote_de_duas_vagas(self):
        self.assertEqual(orcar(Estudio(2)).aluguel_mensal, D("1450.00"))

    def test_vagas_adicionais(self):
        # 1200 + 250 + 3*60 = 1630
        self.assertEqual(orcar(Estudio(5)).aluguel_mensal, D("1630.00"))

    def test_uma_vaga_e_invalido(self):
        with self.assertRaises(ValueError):
            Estudio(1)


class TestTaxaEProjecao(unittest.TestCase):
    def test_parcelas_somam_a_taxa(self):
        for n in range(1, 6):
            self.assertEqual(sum(TaxaContratual(n).valores_parcelas()), D("2000.00"))

    def test_parcelas_com_sobra_de_centavos(self):
        self.assertEqual(
            TaxaContratual(3).valores_parcelas(), [D("666.67"), D("666.67"), D("666.66")]
        )

    def test_parcelamento_invalido(self):
        for n in (0, 6, -1):
            with self.assertRaises(ValueError):
                TaxaContratual(n)

    def test_projecao_tem_12_meses(self):
        proj = orcar(Casa(1, False), parcelas=5).projecao()
        self.assertEqual(len(proj), 12)
        self.assertEqual(proj[0].total_mes, D("1300.00"))   # 900 + 400
        self.assertEqual(proj[4].parcela_taxa, D("400.00"))
        self.assertEqual(proj[5].parcela_taxa, D("0.00"))
        self.assertEqual(proj[11].total_mes, D("900.00"))

    def test_total_geral_do_ano(self):
        # 900*12 + 2000
        self.assertEqual(orcar(Casa(1, False)).total_geral_12_meses, D("12800.00"))


if __name__ == "__main__":
    unittest.main()
