# Modelagem Epidemiológica de Doença Respiratória via Autômato Celular Bidimensional SIR

## Resumo

Este projeto foi desenvolvido para a disciplina optativa de **Modelagem Matemático-Computacional Aplicada à Epidemiologia**. O objetivo é simular, através de um autômato celular (bidimensional de N×N células), a dinâmica de propagação de uma doença infecciosa respiratória utilizando o modelo compartimental **SIR** (Suscetível-Infectado-Recuperado).

A simulação representa três estados epidemiológicos de célula:

* **Suscetível (Azul):** Indivíduos que podem ser infectados pela doença.
* **Infectado (Vermelho):** Indivíduos atualmente infectados e que podem transmitir a doença aos vizinhos.
* **Recuperado (Verde):** Indivíduos que se recuperaram da doença e desenvolveram imunidade (temporária ou permanente).

Ao final da execução, o código:

* Mostra uma animação com a evolução espacial dos estados populacionais.
* Exibe um gráfico temporal com a quantidade de indivíduos em cada estado ao longo dos dias (curvas epidemiológicas S, I e R).

### Regra de Propagação Probabilística

A transmissão segue uma regra probabilística que aumenta com a quantidade de vizinhos infectados na vizinhança de Moore (8 vizinhos). Isso modela realisticamente como doenças respiratórias se propagam por contato próximo, onde múltiplas exposições aumentam significativamente o risco de contaminação.


## Parâmetros ajustáveis

Os parâmetros abaixo podem ser alterados diretamente no início do código (`simulacao_Epidemiologia.py`) para criar diferentes cenários epidemiológicos:

| Parâmetro | Descrição | Valor padrão | Exemplo de alteração |
|-----------|-----------|--------------|----------------------|
| `TAMANHO_GRADE` | Tamanho da grade (NxN) | `50` | `100` para simulação maior |
| `GERACOES` | Número total de dias simulados | `100` | `200` para epidemia mais prolongada |
| `TAXA_TRANSMISSAO` | Probabilidade de transmissão de um vizinho infectado | `0.30` | `0.50` para doença mais contagiosa |
| `TEMPO_BASE_DOENCA` | Dias que a doença dura sem intervenção hospitalar | `20` | `10` para doença mais rápida |
| `PROB_PERDA_IMUNIDADE` | Probabilidade de voltar a ser suscetível após recuperação | `0.03` | `0.00` para imunidade permanente |
| `FATOR_CAPACIDADE_HOSPITALAR` | Redução dias de doença pela intervenção hospitalar | `7` | `0` para sem suporte hospitalar |

O modelo é probabilístico, portanto execuções diferentes podem gerar padrões diferentes, representando a aleatoriedade inerente às epidemias.

#### Parâmetros da Animação

* Dentro da função `executar_simulacao`, você pode alterar o parâmetro `interval` na chamada `FuncAnimation` para diminuir ou aumentar a velocidade da animação.

## 📚 Bibliotecas Utilizadas

O código utiliza as seguintes bibliotecas Python:

- [NumPy](https://numpy.org/) – Manipulação de matrizes e operações numéricas.
- [Matplotlib](https://matplotlib.org/) – Visualização de dados e animação.
- [random](https://docs.python.org/3/library/random.html) – Geração de números aleatórios.

### Instalação das bibliotecas
Você pode instalar todas as dependências executando:

```bash
    pip install numpy matplotlib
```

## ▶️ Execução

1. **Pré-requisitos:**

   * Certifique-se de ter o **Python 3** instalado em seu sistema.

2. **Instale as dependências:**

   * Abra seu terminal ou prompt de comando e execute o seguinte comando para instalar as bibliotecas necessárias:

   ```bash
   pip install numpy matplotlib
   ```

3. **Execute o código:**

   * Navegue pelo terminal até a pasta onde o arquivo `simulacao_Epidemiologia.py` está salvo e execute o comando:

   ```bash
   python simulacao_Epidemiologia.py
   ```

## 🎯 Descrição do Modelo

### Estrutura do Autômato Celular

- **Vizinhança de Moore:** Cada célula interage com seus 8 vizinhos (incluindo diagonais).
- **Atualização Síncrona:** Todas as células são atualizadas simultaneamente a cada geração.
- **Estados Discretos:** Cada célula representa um indivíduo em um dos três compartimentos (S, I ou R).

### Dinâmica de Transição

1. **Suscetível → Infectado:** Um suscetível tem probabilidade de ser infectado proporcionalmente ao número de vizinhos infectados (v). A probabilidade é calculada como: $P(S \to I) = 1 - (1 - TAXA\_TRANSMISSAO)^v$

2. **Infectado → Recuperado:** Um infectado permanece neste estado por um número de dias definido por: $tempo\_cura = \max(1, TEMPO\_BASE\_DOENCA - FATOR\_CAPACIDADE\_HOSPITALAR)$. Maior capacidade hospitalar reduz o tempo de doença.

3. **Recuperado → Suscetível:** Um recuperado pode perder imunidade com probabilidade `PROB_PERDA_IMUNIDADE`, voltando a ser suscetível. Isso permite simular doenças com imunidade temporária.
