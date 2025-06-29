import sys
from instruction_handlers import INSTRUCTION_HANDLERS

def interpretar_bytecode(raw_bytecode_lines):
    pilha = []
    memoria = {}

    # --- Passo 1: Pré-processamento e mapeamento de rótulos (labels) ---
    bytecode = []
    labels = {}
    current_addr = 0 

    for line_num, line in enumerate(raw_bytecode_lines):
        stripped_line = line.strip()
        if not stripped_line:
            continue

        parts = stripped_line.split()
        instrucao = parts[0]

        if instrucao == "LABEL":
            if len(parts) != 2:
                raise ValueError(f"Erro de sintaxe: LABEL requer um nome. Linha: {line_num + 1}")
            label_name = parts[1]
            if label_name in labels:
                raise ValueError(f"Erro: Rótulo '{label_name}' já definido. Linha: {line_num + 1}")
            labels[label_name] = current_addr
        else:
            bytecode.append(parts)
            current_addr += 1

    # --- Passo 2: Interpretação do Bytecode ---
    pc = 0 
    bytecode_len = len(bytecode)

    while pc < bytecode_len:
        current_instruction_parts = bytecode[pc]
        instrucao = current_instruction_parts[0]
        args = current_instruction_parts[1:]

        try:
            if instrucao not in INSTRUCTION_HANDLERS:
                raise ValueError(f"Instrução desconhecida: '{instrucao}'.")

            # Obtém a função manipuladora para a instrução atual
            handler_function = INSTRUCTION_HANDLERS[instrucao]

            # Chama a função manipuladora, passando todos os estados necessários
            # A função retornará o novo valor do PC ou o incremento
            new_pc_or_increment = handler_function(
                pilha, memoria, pc, bytecode_len, labels, args
            )

            # Atualiza o PC baseado no retorno da função manipuladora
            if new_pc_or_increment == -1: # Sinal para HALT
                return
            elif instrucao in ["JMP", "JZ", "JNZ", "CALL", "RET"]:
                # Funções de controle de fluxo retornam o PC direto
                pc = new_pc_or_increment
            else:
                # Outras funções retornam o incremento (geralmente 1)
                pc += new_pc_or_increment

        except Exception as e:
            sys.stderr.write(f"Erro durante a execução na linha de bytecode {pc} (instrução '{instrucao}'): {e}\n")
            sys.exit(1)

def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                bytecode_lines = f.readlines()
            interpretar_bytecode(bytecode_lines)
        except FileNotFoundError:
            sys.stderr.write(f"Erro: Arquivo '{sys.argv[1]}' não encontrado.\n")
            sys.exit(1)
        except ValueError as e: 
            sys.stderr.write(f"Erro de pré-processamento/parsing: {e}\n")
            sys.exit(1)
        except Exception as e:
            sys.stderr.write(f"Erro inesperado: {e}\n")
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            print("Insira o bytecode na entrada padrão:")
        bytecode_lines = sys.stdin.read().splitlines()
        try:
            interpretar_bytecode(bytecode_lines)
        except ValueError as e:
            sys.stderr.write(f"Erro de pré-processamento/parsing: {e}\n")
            sys.exit(1)
        except Exception as e:
            sys.stderr.write(f"Erro inesperado: {e}\n")
            sys.exit(1)

if __name__ == "__main__":
    main()