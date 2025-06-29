# Interpretador de Bytecode

## 1\. Contexto da Disciplina de Compiladores

Este trabalho prático aborda conceitos fundamentais estudados na disciplina de Compiladores, focando especificamente na **Geração de Código Intermediário** e na **Máquina Virtual (Runtime)**.

  * **Máquina Virtual (VM):** O interpretador simula uma máquina virtual, que é um ambiente de execução abstrato. Nossa VM é uma máquina de pilha simples, onde as operações manipulam valores diretamente em uma estrutura de pilha.
  * **Bytecode como Representação Intermediária:** O código de entrada para o nosso interpretador é o "bytecode". Este representa uma **linguagem intermediária** entre a linguagem de alto nível (que não implementamos o compilador aqui) e a execução final. Ele é mais abstrato que o código de máquina nativo, mas mais concreto que a linguagem-fonte, facilitando a portabilidade e a interpretação.
  * **Ambiente de Tempo de Execução (Runtime Environment):** O interpretador gerencia os componentes cruciais de um ambiente de tempo de execução:
      * **Pilha (Stack):** Usada para operações aritméticas, passagem de parâmetros e gerenciamento de endereços de retorno de funções.
      * **Memória (Heap/Variáveis):** Simulada por um dicionário, onde as variáveis do programa são armazenadas.
      * **Contador de Programa (Program Counter - PC):** Controla o fluxo de execução, apontando para a próxima instrução a ser processada.
  * **Análise de Fluxo de Controle:** As instruções de salto (`JMP`, `JZ`, `JNZ`), chamada (`CALL`) e retorno (`RET`) demonstram como o fluxo de controle de um programa é gerenciado e alterado durante a execução, essencial para estruturas como `if/else`, `loops` e `funções`.
  * **Tabela de Símbolos (implícita):** O dicionário de `labels` (rótulos) e o dicionário `memoria` (para variáveis) atuam como formas de tabela de símbolos em tempo de execução, mapeando identificadores (rótulos, nomes de variáveis) para seus respectivos endereços ou valores.
  * **Arquitetura de Pilha (Stack Architecture):** A escolha de uma máquina de pilha simplifica a lógica das operações aritméticas e o gerenciamento de chamadas de função, pois a maioria dos operandos é implicitamente retirada e os resultados são empilhados.

## 2\. Especificação da Linguagem (Tiny Language)

A "tiny language" é uma linguagem de máquina de pilha com as seguintes funcionalidades:

  * **Operações Aritméticas e de Pilha:** `PUSH`, `POP`, `ADD`, `SUB`, `MUL`, `DIV`, `MOD`, `NEG`.
  * **Declaração e Manipulação de Variáveis:** `STORE`, `LOAD`.
  * **Fluxo de Controle:** `JMP` (salto incondicional), `JZ` (salto se zero), `JNZ` (salto se não zero), `HALT` (finaliza a execução).
  * **Comparações:** `EQ` (igual), `NEQ` (diferente), `LT` (menor que), `GT` (maior que), `LE` (menor ou igual), `GE` (maior ou igual).
  * **Chamadas de Função e I/O:** `CALL`, `RET`, `PRINT` (saída padrão), `READ` (entrada padrão).
  * **Rótulos:** `LABEL <nome_rotulo>` (usados como alvos para instruções de salto).

## 3\. Arquitetura do Interpretador

O interpretador é implementado em Python e segue uma arquitetura modular:

  * **Fase de Pré-processamento:** Antes da execução, o interpretador realiza uma primeira passagem pelo código bytecode.
      * Identifica e mapeia todos os `LABEL`s para seus respectivos endereços (índices na lista de instruções executáveis).
      * Ignora linhas vazias.
      * Verifica erros de rótulo duplicado ou sintaxe de `LABEL`.
  * **Loop de Execução Principal:** Um loop `while` controlado por um `Program Counter (pc)` que itera sobre as instruções do bytecode.
  * **Dicionário de Despacho de Instruções:** Para simular uma estrutura `switch-case` em Python de forma eficiente e limpa, utilizamos um dicionário (`INSTRUCTION_HANDLERS`) que mapeia o nome de cada instrução para uma função Python específica responsável por sua execução. Isso torna o código principal conciso e facilita a adição/modificação de instruções.
  * **Funções Manipuladoras (Handlers):** Cada instrução possui uma função dedicada que manipula a pilha, a memória e o `pc` conforme a semântica da instrução.
  * **Tratamento de Erros:** O interpretador inclui tratamento de erros robusto para situações como:
      * Stack Underflow (tentar `POP` em pilha vazia).
      * Divisão/Módulo por zero.
      * Variável não definida (`LOAD` de variável inexistente).
      * Sintaxe inválida de instruções (número incorreto de argumentos).
      * Saltos para endereços fora dos limites do programa.
      * Instruções desconhecidas.

## 4\. Estrutura do Projeto

O projeto está dividido em dois arquivos principais para promover a modularidade:

  * `interpretador.py`: Contém a lógica principal do interpretador, incluindo o pré-processamento de rótulos, o loop de execução e o gerenciamento do `Program Counter`, além da função `main` para entrada/saída.
  * `instruction_handlers.py`: Contém as funções Python que implementam a semântica de cada instrução do bytecode, bem como o dicionário `INSTRUCTION_HANDLERS` que as mapeia.

## 5\. Como Rodar o Interpretador

### Pré-requisitos

  * Python 3.10 ou superior (necessário para a sintaxe `match-case` utilizada).

### Execução

Você pode fornecer o bytecode de duas maneiras:

1.  **Via Entrada Padrão (stdin):**

    ```bash
    python interpretador.py
    ```

    O interpretador solicitará que você insira o bytecode. Após colar ou digitar o código, finalize a entrada:

      * **Linux/macOS:** `Ctrl + D`
      * **Windows:** `Ctrl + Z` seguido de `Enter`

2.  **Via Arquivo (recomendado para programas maiores):**
    Crie um arquivo de texto (ex: `meu_programa.bytecode`) contendo seu código bytecode.

    ```bash
    # Exemplo:
    # meu_programa.bytecode
    # PUSH 10
    # PUSH 2
    # MUL
    # PRINT
    # HALT

    python interpretador.py meu_programa.bytecode
    ```

    O interpretador lerá o conteúdo do arquivo, executará-o e exibirá a saída no terminal.

