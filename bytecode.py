import sys

def interpretar_bytecode(raw_bytecode_lines):
    pilha = []  # Pilha principal para operações e valores
    memoria = {}  # Dicionário para armazenar variáveis 

    # --- Passo 1: Pré-processamento e mapeamento de rótulos (labels) ---
    # Cria uma lista limpa de instruções executáveis e um mapa de rótulos para seus endereços
    bytecode = []
    labels = {}
    current_addr = 0 # O endereço da instrução no array 'bytecode'

    for line_num, line in enumerate(raw_bytecode_lines):
        stripped_line = line.strip()
        if not stripped_line: # Ignora linhas vazias
            continue

        parts = stripped_line.split()
        instrucao = parts[0]

        if instrucao == "LABEL": # Rótulos não são instruções executáveis, mas marcam um endereço 
            if len(parts) != 2:
                raise ValueError(f"Erro de sintaxe: LABEL requer um nome. Linha: {line_num + 1}: '{line}'")
            label_name = parts[1]
            if label_name in labels:
                raise ValueError(f"Erro: Rótulo '{label_name}' já definido. Linha: {line_num + 1}")
            labels[label_name] = current_addr # Armazena o endereço onde este rótulo aponta
        else:
            # Armazena a instrução real para execução
            bytecode.append(parts)
            current_addr += 1 # Incrementa o endereço apenas para instruções reais

    # --- Passo 2: Interpretação do Bytecode ---
    pc = 0 # Program Counter: Apontador para a próxima instrução a ser executada 

    while pc < len(bytecode):
        current_instruction_parts = bytecode[pc]
        instrucao = current_instruction_parts[0]
        args = current_instruction_parts[1:] # Argumentos da instrução

        try:
            if instrucao == "PUSH":
                if len(args) != 1:
                    raise ValueError(f"Sintaxe inválida para PUSH. Uso: PUSH <valor>. Linha: {pc}")
                valor = int(args[0])
                pilha.append(valor)  
                pc += 1

            elif instrucao == "POP":
                if not pilha:
                    raise IndexError("POP em pilha vazia.")  
                pilha.pop()  
                pc += 1

            elif instrucao == "ADD":
                if len(pilha) < 2:
                    raise IndexError("ADD requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(a + b)  
                pc += 1

            elif instrucao == "SUB":
                if len(pilha) < 2:
                    raise IndexError("SUB requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(a - b)  
                pc += 1

            elif instrucao == "MUL":
                if len(pilha) < 2:
                    raise IndexError("MUL requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(a * b)  
                pc += 1

            elif instrucao == "DIV":
                if len(pilha) < 2:
                    raise IndexError("DIV requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                if b == 0:
                    raise ZeroDivisionError("Divisão por zero.")
                pilha.append(a // b) # Divisão inteira  
                pc += 1

            elif instrucao == "MOD":
                if len(pilha) < 2:
                    raise IndexError("MOD requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                if b == 0:
                    raise ZeroDivisionError("Módulo por zero.")
                pilha.append(a % b)  
                pc += 1

            elif instrucao == "NEG":
                if not pilha:
                    raise IndexError("NEG requer um valor na pilha.")  
                val = pilha.pop()  
                pilha.append(-val)  
                pc += 1

            elif instrucao == "STORE":
                if len(args) != 1:
                    raise ValueError(f"Sintaxe inválida para STORE. Uso: STORE <nome_variavel>. Linha: {pc}")
                if not pilha:
                    raise IndexError("STORE requer um valor na pilha para armazenar.")   
                nome = args[0]
                memoria[nome] = pilha.pop() # Desempilha o valor e salva na memória 
                pc += 1

            elif instrucao == "LOAD":
                if len(args) != 1:
                    raise ValueError(f"Sintaxe inválida para LOAD. Uso: LOAD <nome_variavel>. Linha: {pc}")
                nome = args[0]
                if nome not in memoria:
                    raise NameError(f"Variável '{nome}' não definida.")
                pilha.append(memoria[nome]) # Empilha o valor da variável carregada 
                pc += 1

            elif instrucao == "JMP":
                if len(args) != 1:
                    raise ValueError(f"Sintaxe inválida para JMP. Uso: JMP <endereco_ou_rotulo>. Linha: {pc}")
                target = args[0]
                if target in labels:
                    pc = labels[target]
                else:
                    try:
                        numeric_target = int(target)
                        if not (0 <= numeric_target < len(bytecode)):
                            raise ValueError(f"Endereço de pulo '{numeric_target}' fora dos limites do programa.")
                        pc = numeric_target
                    except ValueError:
                        raise ValueError(f"Alvo de JMP inválido: '{target}'. Linha: {pc}")

            elif instrucao == "JZ":
                if len(args) != 1:
                    raise ValueError(f"Sintaxe inválida para JZ. Uso: JZ <endereco_ou_rotulo>. Linha: {pc}")
                if not pilha:
                    raise IndexError("JZ requer um valor na pilha para verificar a condição.")    
                condition = pilha.pop()    
                if condition == 0: # Se o valor desempilhado for zero
                    target = args[0]
                    if target in labels:
                        pc = labels[target]
                    else:
                        try:
                            numeric_target = int(target)
                            if not (0 <= numeric_target < len(bytecode)):
                                raise ValueError(f"Endereço de pulo '{numeric_target}' fora dos limites do programa.")
                            pc = numeric_target
                        except ValueError:
                            raise ValueError(f"Alvo de JZ inválido: '{target}'. Linha: {pc}")
                else:
                    pc += 1 # Continua para a próxima instrução

            elif instrucao == "JNZ":
                if len(args) != 1:
                    raise ValueError(f"Sintaxe inválida para JNZ. Uso: JNZ <endereco_ou_rotulo>. Linha: {pc}")
                if not pilha:
                    raise IndexError("JNZ requer um valor na pilha para verificar a condição.")    
                condition = pilha.pop()    
                if condition != 0: # Se o valor desempilhado não for zero
                    target = args[0]
                    if target in labels:
                        pc = labels[target]
                    else:
                        try:
                            numeric_target = int(target)
                            if not (0 <= numeric_target < len(bytecode)):
                                raise ValueError(f"Endereço de pulo '{numeric_target}' fora dos limites do programa.")
                            pc = numeric_target
                        except ValueError:
                            raise ValueError(f"Alvo de JNZ inválido: '{target}'. Linha: {pc}")
                else:
                    pc += 1 # Continua para a próxima instrução

            elif instrucao == "HALT":
                return # Encerra a execução do programa    

            elif instrucao == "EQ":
                if len(pilha) < 2:
                    raise IndexError("EQ requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(1 if a == b else 0)  
                pc += 1

            elif instrucao == "NEQ":
                if len(pilha) < 2:
                    raise IndexError("NEQ requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(1 if a != b else 0)  
                pc += 1

            elif instrucao == "LT":
                if len(pilha) < 2:
                    raise IndexError("LT requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(1 if a < b else 0)  
                pc += 1

            elif instrucao == "GT":
                if len(pilha) < 2:
                    raise IndexError("GT requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(1 if a > b else 0)  
                pc += 1

            elif instrucao == "LE":
                if len(pilha) < 2:
                    raise IndexError("LE requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(1 if a <= b else 0)  
                pc += 1

            elif instrucao == "GE":
                if len(pilha) < 2:
                    raise IndexError("GE requer dois valores na pilha.")  
                b = pilha.pop()  
                a = pilha.pop()  
                pilha.append(1 if a >= b else 0)  
                pc += 1

            elif instrucao == "CALL":
                if len(args) != 1:
                    raise ValueError(f"Sintaxe inválida para CALL. Uso: CALL <endereco_ou_rotulo>. Linha: {pc}")
                # Empilha o endereço de retorno (próxima instrução) na pilha 
                pilha.append(pc + 1)
                target = args[0]
                if target in labels:
                        pc = labels[target]
                else:
                    try:
                        numeric_target = int(target)
                        if not (0 <= numeric_target < len(bytecode)):
                            raise ValueError(f"Endereço de pulo '{numeric_target}' fora dos limites do programa.")
                        pc = numeric_target
                    except ValueError:
                        raise ValueError(f"Alvo de CALL inválido: '{target}'. Linha: {pc}")

            elif instrucao == "RET":
                if not pilha:
                    raise IndexError("RET em pilha vazia (nenhum endereço de retorno para desempilhar).")  
                pc = pilha.pop() # Desempilha o endereço de retorno e pula para ele 

            elif instrucao == "PRINT":
                if not pilha:
                    raise IndexError("PRINT requer um valor na pilha para imprimir.")  
                print(pilha[-1]) # Imprime o valor no topo da pilha (sem desempilhar, conforme exemplo)  
                pc += 1

            elif instrucao == "READ":
                if len(args) != 0:
                    raise ValueError(f"Sintaxe inválida para READ. Uso: READ. Linha: {pc}")
                try:
                    val = int(input()) # Lê um inteiro da entrada padrão 
                    pilha.append(val)  
                except ValueError:
                    raise ValueError(f"Entrada inválida para READ (esperava um inteiro). Linha: {pc}")
                pc += 1

            else:
                raise ValueError(f"Instrução desconhecida: '{instrucao}'. Linha: {pc}")
        except Exception as e:
            # Captura exceções e adiciona a linha do bytecode para depuração
            sys.stderr.write(f"Erro durante a execução da instrução '{instrucao}' na linha de bytecode {pc} (código original pode variar): {e}\n")
            sys.exit(1) # Sai com erro

def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                bytecode_lines = f.readlines()
        except FileNotFoundError:
            sys.stderr.write(f"Erro: Arquivo '{sys.argv[1]}' não encontrado.\n")
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            print("Insira o bytecode na entrada padrão:")
        bytecode_lines = sys.stdin.read().splitlines()

    interpretar_bytecode(bytecode_lines)

if __name__ == "__main__":
    main()