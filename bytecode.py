import sys

def interpretar_bytecode(bytecode):
    pilha = []
    memoria = {}  # dicionário para armazenar variáveis

    for linha in bytecode:
        partes = linha.strip().split()

        if not partes:
            continue

        instrucao = partes[0]

        if instrucao == "PUSH":
            if len(partes) != 2:
                raise ValueError(f"Erro de sintaxe: {linha}")
            valor = int(partes[1])
            pilha.append(valor)

        elif instrucao == "POP":
            if not pilha:
                raise IndexError("POP em pilha vazia")
            pilha.pop()

        elif instrucao == "ADD":
            if len(pilha) < 2:
                raise IndexError("ADD requer dois valores na pilha")
            b = pilha.pop()
            a = pilha.pop()
            pilha.append(a + b)

        elif instrucao == "SUB":
            if len(pilha) < 2:
                raise IndexError("SUB requer dois valores na pilha")
            b = pilha.pop()
            a = pilha.pop()
            pilha.append(a - b)

        elif instrucao == "MUL":
            if len(pilha) < 2:
                raise IndexError("MUL requer dois valores na pilha")
            b = pilha.pop()
            a = pilha.pop()
            pilha.append(a * b)

        elif instrucao == "DIV":
            if len(pilha) < 2:
                raise IndexError("DIV requer dois valores na pilha")
            b = pilha.pop()
            a = pilha.pop()
            if b == 0:
                raise ZeroDivisionError("Divisão por zero")
            pilha.append(a // b)

        elif instrucao == "STORE":
            if len(partes) != 2:
                raise ValueError("Uso: STORE <nome_variavel>")
            if not pilha:
                raise IndexError("STORE requer valor na pilha")
            nome = partes[1]
            memoria[nome] = pilha.pop()

        elif instrucao == "LOAD":
            if len(partes) != 2:
                raise ValueError("Uso: LOAD <nome_variavel>")
            nome = partes[1]
            if nome not in memoria:
                raise NameError(f"Variável '{nome}' não definida")
            pilha.append(memoria[nome])

        elif instrucao == "PRINT":
            if not pilha:
                raise IndexError("PRINT requer pelo menos um valor na pilha")
            print(pilha[-1])

        else:
            raise ValueError(f"Instrução desconhecida: {instrucao}")

def main():
    if sys.stdin.isatty():
        print("Insira o bytecode na entrada padrão (CTRL+D para encerrar):")
    bytecode = sys.stdin.read().splitlines()
    interpretar_bytecode(bytecode)

if __name__ == "__main__":
    main()
