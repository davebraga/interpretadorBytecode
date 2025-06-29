def _handle_push(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(args) != 1:
        raise ValueError(f"Sintaxe inválida para PUSH. Uso: PUSH <valor>.")
    valor = int(args[0])
    pilha.append(valor)
    return 1 

def _handle_pop(pilha, memoria, current_pc, bytecode_len, labels, args):
    if not pilha:
        raise IndexError("POP em pilha vazia.")
    pilha.pop()
    return 1

def _handle_add(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2:
        raise IndexError("ADD requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(a + b)
    return 1

def _handle_sub(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2:
        raise IndexError("SUB requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(a - b)
    return 1

def _handle_mul(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2:
        raise IndexError("MUL requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(a * b)
    return 1

def _handle_div(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2:
        raise IndexError("DIV requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    if b == 0:
        raise ZeroDivisionError("Divisão por zero.")
    pilha.append(a // b)
    return 1

def _handle_mod(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2:
        raise IndexError("MOD requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    if b == 0:
        raise ZeroDivisionError("Módulo por zero.")
    pilha.append(a % b)
    return 1

def _handle_neg(pilha, memoria, current_pc, bytecode_len, labels, args):
    if not pilha:
        raise IndexError("NEG requer um valor na pilha.")
    val = pilha.pop()
    pilha.append(-val)
    return 1

def _handle_store(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(args) != 1:
        raise ValueError("Sintaxe inválida para STORE. Uso: STORE <nome_variavel>.")
    if not pilha:
        raise IndexError("STORE requer um valor na pilha para armazenar.")
    nome = args[0]
    memoria[nome] = pilha.pop()
    return 1

def _handle_load(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(args) != 1:
        raise ValueError("Sintaxe inválida para LOAD. Uso: LOAD <nome_variavel>.")
    nome = args[0]
    if nome not in memoria:
        raise NameError(f"Variável '{nome}' não definida.")
    pilha.append(memoria[nome])
    return 1

def _handle_jmp(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(args) != 1:
        raise ValueError(f"Sintaxe inválida para JMP. Uso: JMP <endereco_ou_rotulo>.")
    target = args[0]
    if target in labels:
        return labels[target]
    else:
        try:
            numeric_target = int(target)
            if not (0 <= numeric_target < bytecode_len):
                raise ValueError(f"Endereço de pulo '{numeric_target}' fora dos limites do programa.")
            return numeric_target
        except ValueError:
            raise ValueError(f"Alvo de JMP inválido: '{target}'.")

def _handle_jz(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(args) != 1:
        raise ValueError(f"Sintaxe inválida para JZ. Uso: JZ <endereco_ou_rotulo>.")
    if not pilha:
        raise IndexError("JZ requer um valor na pilha para verificar a condição.")
    condition = pilha.pop()
    if condition == 0:
        target = args[0]
        if target in labels:
            return labels[target]
        else:
            try:
                numeric_target = int(target)
                if not (0 <= numeric_target < bytecode_len):
                    raise ValueError(f"Endereço de pulo '{numeric_target}' fora dos limites do programa.")
                return numeric_target
            except ValueError:
                raise ValueError(f"Alvo de JZ inválido: '{target}'.")
    else:
        return current_pc + 1

def _handle_jnz(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(args) != 1:
        raise ValueError(f"Sintaxe inválida para JNZ. Uso: JNZ <endereco_ou_rotulo>.")
    if not pilha:
        raise IndexError("JNZ requer um valor na pilha para verificar a condição.")
    condition = pilha.pop()
    if condition != 0:
        target = args[0]
        if target in labels:
            return labels[target]
        else:
            try:
                numeric_target = int(target)
                if not (0 <= numeric_target < bytecode_len):
                    raise ValueError(f"Endereço de pulo '{numeric_target}' fora dos limites do programa.")
                return numeric_target
            except ValueError:
                raise ValueError(f"Alvo de JNZ inválido: '{target}'.")
    else:
        return current_pc + 1

def _handle_halt(pilha, memoria, current_pc, bytecode_len, labels, args):
    return -1 # Sinaliza para o loop principal parar

def _handle_eq(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2: raise IndexError("EQ requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(1 if a == b else 0)
    return 1

def _handle_neq(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2: raise IndexError("NEQ requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(1 if a != b else 0)
    return 1

def _handle_lt(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2: raise IndexError("LT requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(1 if a < b else 0)
    return 1

def _handle_gt(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2: raise IndexError("GT requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(1 if a > b else 0)
    return 1

def _handle_le(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2: raise IndexError("LE requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(1 if a <= b else 0)
    return 1

def _handle_ge(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(pilha) < 2: raise IndexError("GE requer dois valores na pilha.")
    b = pilha.pop()
    a = pilha.pop()
    pilha.append(1 if a >= b else 0)
    return 1

def _handle_call(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(args) != 1:
        raise ValueError(f"Sintaxe inválida para CALL. Uso: CALL <endereco_ou_rotulo>.")
    pilha.append(current_pc + 1) # Empilha o endereço de retorno
    target = args[0]
    if target in labels:
        return labels[target]
    else:
        try:
            numeric_target = int(target)
            if not (0 <= numeric_target < bytecode_len):
                raise ValueError(f"Endereço de pulo '{numeric_target}' fora dos limites do programa.")
            return numeric_target
        except ValueError:
            raise ValueError(f"Alvo de CALL inválido: '{target}'.")

def _handle_ret(pilha, memoria, current_pc, bytecode_len, labels, args):
    if not pilha:
        raise IndexError("RET em pilha vazia (nenhum endereço de retorno para desempilhar).")
    return pilha.pop() # Desempilha o endereço de retorno e retorna como o novo PC

def _handle_print(pilha, memoria, current_pc, bytecode_len, labels, args):
    if not pilha:
        raise IndexError("PRINT requer um valor na pilha para imprimir.")
    print(pilha[-1]) # Imprime o valor no topo da pilha (sem desempilhar)
    return 1

def _handle_read(pilha, memoria, current_pc, bytecode_len, labels, args):
    if len(args) != 0:
        raise ValueError(f"Sintaxe inválida para READ. Uso: READ.")
    try:
        val = int(input())
        pilha.append(val)
    except ValueError:
        raise ValueError(f"Entrada inválida para READ (esperava um inteiro).")
    return 1

# Dicionário de despacho de instruções
INSTRUCTION_HANDLERS = {
    "PUSH": _handle_push,
    "POP": _handle_pop,
    "ADD": _handle_add,
    "SUB": _handle_sub,
    "MUL": _handle_mul,
    "DIV": _handle_div,
    "MOD": _handle_mod,
    "NEG": _handle_neg,
    "STORE": _handle_store,
    "LOAD": _handle_load,
    "JMP": _handle_jmp,
    "JZ": _handle_jz,
    "JNZ": _handle_jnz,
    "HALT": _handle_halt,
    "EQ": _handle_eq,
    "NEQ": _handle_neq,
    "LT": _handle_lt,
    "GT": _handle_gt,
    "LE": _handle_le,
    "GE": _handle_ge,
    "CALL": _handle_call,
    "RET": _handle_ret,
    "PRINT": _handle_print,
    "READ": _handle_read,
}