# RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)

Aplicação em Python, com Programação Orientada a Objetos, que calcula o orçamento de locação de apartamentos, casas e estúdios da **R.M Imóveis**, exibe um resumo detalhado e gera um **CSV com a projeção dos 12 primeiros meses** do contrato.

Disciplina: *Algorithmic Thinking & Introduction to Object-Oriented Programming*.

## Requisitos

- Python **3.10 ou superior**.

## Como executar

```bash
# 1. Clone o repositório e entre na pasta
git clone <URL-DO-REPOSITORIO>
cd rentsmart

# 2. Execute o programa
python main.py          # no Windows também: py main.py
```

O programa pergunta, em sequência: nome do cliente, tipo de imóvel, características (quartos, garagem, crianças ou estacionamento, conforme o tipo) e o parcelamento da taxa contratual (1 a 5 vezes). Em seguida mostra o orçamento no terminal e grava o arquivo **`projecao_locacao_12_meses.csv`** na pasta atual.

### Executar os testes automatizados

```bash
python -m unittest -v
```

## Regras de negócio implementadas

| Item | Regra |
|---|---|
| Aluguel-base | Apartamento 1 quarto: R$ 700,00 · Casa 1 quarto: R$ 900,00 · Estúdio: R$ 1.200,00 |
| Segundo quarto | Apartamento: +R$ 200,00 · Casa: +R$ 250,00 (estúdio não tem essa opção) |
| Garagem (casa/apartamento) | +R$ 300,00 por mês (uma vaga) |
| Estacionamento do estúdio | Pacote inicial de 2 vagas: R$ 250,00 · cada vaga adicional: +R$ 60,00 |
| Desconto | Apenas apartamento: 5% sobre o aluguel **já com os adicionais**, se o cliente não tiver crianças |
| Taxa contratual | R$ 2.000,00, parcelável em até 5 vezes, exibida **separadamente** do aluguel |

### Premissas adotadas (onde o enunciado deixa margem)

- **Estacionamento do estúdio é opcional.** Se contratado, o mínimo é 2 vagas (o pacote inicial); 1 vaga é rejeitada. A partir da 3ª vaga, cada uma custa R$ 60,00.
- **Parcelas da taxa** são cobradas nos primeiros meses do contrato (parcela 1 no mês 1, e assim por diante). Quando a divisão não é exata (ex.: 3 × R$ 666,67), os centavos de sobra vão para as primeiras parcelas, de modo que a soma seja sempre exatamente R$ 2.000,00.
- O **aluguel é fixo nos 12 meses** (não há reajuste previsto nas regras).
- Valores monetários usam `Decimal` (não `float`) para evitar erros de arredondamento.

## Arquitetura (classes)

```
Imovel (abstrata)                       imoveis.py
├── ImovelResidencial (abstrata)        quartos + garagem (regras comuns)
│   ├── Apartamento                     + desconto de 5% sem crianças
│   └── Casa
└── Estudio                             pacote de estacionamento próprio

ItemValor            linha do orçamento (descrição + valor)        imoveis.py
TaxaContratual       taxa de R$ 2.000 e divisão em parcelas       orcamento.py
Orcamento            calcula aluguel, desconto, projeção          orcamento.py
LinhaProjecao        um mês da projeção                           orcamento.py
ExportadorCSV        grava a projeção em CSV                      exportador.py
EntradaUsuario       leitura e validação das entradas             interface.py
ApresentadorOrcamento monta o resumo exibido ao cliente           interface.py
AplicacaoRentSmart   orquestra o fluxo do programa                main.py
```

Principais decisões:

- **Herança e polimorfismo:** cada tipo de imóvel conhece suas próprias regras de preço (`adicionais()`, `percentual_desconto()`). O `Orcamento` trabalha com qualquer `Imovel` sem `if` por tipo.
- **Sem repetição:** casa e apartamento compartilham quartos e garagem em `ImovelResidencial`; só diferem no adicional do 2º quarto e no desconto.
- **Separação de responsabilidades:** regras de negócio (`imoveis.py`, `orcamento.py`) não dependem de `input()`/`print()`; a interface, a exportação e o fluxo ficam em módulos próprios. Isso também permite testar as regras isoladamente (`test_rentsmart.py`).
- **Validação:** entradas inválidas na interface são pedidas novamente; as próprias classes de domínio também lançam `ValueError` para valores impossíveis (ex.: 3 quartos, 7 parcelas).

## Arquivo CSV gerado

Formato compatível com o Excel em português: separador `;`, vírgula decimal e UTF-8 com BOM.

| mes | aluguel_mensal | parcela_taxa_contratual | total_do_mes |
|---|---|---|---|
| 1 | 1140,00 | 400,00 | 1540,00 |
| … | … | … | … |
| 12 | 1140,00 | 0,00 | 1140,00 |

Um exemplo real de saída está em `exemplo_projecao_locacao_12_meses.csv` (apartamento de 2 quartos, com garagem, sem crianças, taxa em 5 parcelas).

## Estrutura do repositório

```
rentsmart/
├── main.py
├── imoveis.py
├── orcamento.py
├── exportador.py
├── interface.py
├── dinheiro.py
├── test_rentsmart.py
├── exemplo_projecao_locacao_12_meses.csv
└── README.md
```
