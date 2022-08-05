from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, Aer, execute


def hello():
    print('Hello, it\'s me!')

    
def cmp_qq(n_1, type, n_2):
    
    # '''Compares digits stored in qubits of input 1 and input 2.
    # Requires (n_1 + n_2 + 1) qubits if switches qubit as a result (phase_shift = False).
    # Requires (n_1 + n_2) qubits if shifts phase as a result (phase_shift = True).
    # Operation types (type): "=", "!=", ">", ">=", "<", "<=".
    # - n_1 — first input qubits
    # - n_2 — second input qubits
    # - 1 — qubit for result (phase_shift = False or doesn\'t set)'''

    '''Compares digits stored in qubits of input 1 and input 2.
    Operation types (type): "=", "!=", ">", ">=", "<", "<="
    Requires (n_1 + n_2 + 1) qubits:
    - n_1 — first input qubits
    - n_2 — second input qubits
    - 1 — qubit for the result'''
    
    def if_not_equal(inp_1, inp_2):

        l = len(inp_1) if len(inp_1) < len(inp_2) else len(inp_2)
        
        shr_n_1, shr_n_2 = inp_1[0:l], inp_2[0:l]
        
        exq = []
        e = 0
        
        if len(inp_1) > len(inp_2):
            e = len(inp_1) - len(inp_2)
            exq = inp_1[l:]
        elif len(inp_2) > len(inp_1):
            e = len(inp_2) - len(inp_1)
            exq = inp_2[l:]

        for i in reversed(range(e)):
            circuit.mcx([*exq[i:e]], result)
            circuit.x(exq[i])

        for i in range(l):
            circuit.mcx([*exq, shr_n_1[i]], shr_n_2[i])
        
        for i in range(l):
            circuit.mcx([*exq, *shr_n_2[0:i+1]], result)
            if i < l-1:
                circuit.x(shr_n_2[i])
        
        circuit.x(shr_n_2[:-1])

        for i in range(l):
            circuit.mcx([*exq, shr_n_1[i]], shr_n_2[i])
        
        if len(exq) > 0:
            circuit.x(exq)

    def if_1_grt_2(inp_1, inp_2):

        l = len(inp_1) if len(inp_1) < len(inp_2) else len(inp_2)
        
        shr_n_1, shr_n_2 = inp_1[0:l], inp_2[0:l]
        
        exq = []
        e = 0
        
        if len(inp_1) > len(inp_2):
            e = len(inp_1) - len(inp_2)
            exq = inp_1[l:]
            for i in reversed(range(e)):
                circuit.mcx([*exq[i:e]], result)
                circuit.x(exq[i])
        elif len(inp_2) > len(inp_1):
            e = len(inp_2) - len(inp_1)
            exq = inp_2[l:]
            circuit.x(exq)

        for i in range(l):
            circuit.mcx([*exq, shr_n_1[i]], shr_n_2[i])
            k = l - i
            for j in range(k):
                if j + i > l-2:
                    circuit.mcx([*exq, shr_n_1[i], *shr_n_2[i : i + j + 2]], result)
                else:
                    circuit.mcx([*exq, shr_n_1[i], *shr_n_2[i : i + j + 1]], shr_n_2[i + j + 1])
                    
        for i in reversed(range(l)):
            k = l - i
            for j in reversed(range(k)):
                if j + i > l-2:
                    pass
                else:
                    circuit.mcx([*exq, shr_n_1[i], *shr_n_2[i : i + j + 1]], shr_n_2[i + j + 1])
                    
            circuit.mcx([*exq, shr_n_1[i]], shr_n_2[i])

        if len(exq) > 0:
            circuit.x(exq)
    
    actions = {
        '=': if_not_equal,
        '!=': if_not_equal,
        '>': if_1_grt_2,
        '>=': if_1_grt_2,
        '<': if_1_grt_2,
        '<=': if_1_grt_2,
    }

    qubits = QuantumRegister(n_1 + n_2 + 1)
    circuit = QuantumCircuit(qubits)
    
    input_1 = qubits[0 : n_1]
    input_2 = qubits[n_1 : n_1 + n_2]

    result = qubits[n_1 + n_2]

    if type == '=' or type == '<=' or type == '>=':
        circuit.x(result)
    
    if type == '<' or type == '>=':
        actions[type](input_2, input_1)
    else:
        actions[type](input_1, input_2)

    return circuit


def cmp_qd(n, type, number):
    
    '''Compares digit stored in qubits of input with exact digit.
    Operation types (type): "=", "!=", ">", ">=", "<", "<="
    Requires (n + 1) qubits:
    - n — input qubits
    - 1 — qubit for result'''

    def if_equal():

        for i in range(n):
            if number_bits[n - i - 1] == '0':
                circuit.x(i)
        
        circuit.mct(list(range(n)), n)

        for i in range(n):
            if number_bits[n - i - 1] == '0':
                circuit.x(i)

    def if_less_not_equal():

        for i in range(n):
            if number_bits[n - i - 1] == '1':
                circuit.x(input[i : n])
                break
        
        for i in range(n):
            if number_bits[i] == '1':
                circuit.mct(input[n - i - 1 : n], result)
                circuit.x(input[n - i - 1])

        for i in range(n):
            if number_bits[n - i - 1] == '1':
                for j in range(i, n):
                    if number_bits[n - j - 1] == '0':
                        circuit.x(input[j])
                break

    def if_less_and_equal():

        for i in range(n):
            if number_bits[n - i - 1] == '1':
                circuit.x(input[i : n])
                break
        
        for i in range(n):
            if number_bits[i] == '1':
                circuit.mct(input[n - i - 1 : n], result)
                circuit.x(input[n - i - 1])

        for i in range(n):
            if number_bits[n - i - 1] == '1':
                for j in range(i, n):
                    if number_bits[n - j - 1] == '0':
                        circuit.x(input[j])
                break

        for i, bit in enumerate(reversed(number_bits)):
            if bit == '0':
                circuit.x(i)
        
        circuit.mcx(input, result)

        for i, bit in enumerate(reversed(number_bits)):
            if bit == '0':
                circuit.x(i)
    
    actions = {
        '=': if_equal,
        '!=': if_equal,
        '>': if_less_and_equal,
        '>=': if_less_not_equal,
        '<': if_less_not_equal,
        '<=': if_less_and_equal,
    }

    number_bits = str(bin(number))[2:]
    assert len(number_bits) <= n, 'Not enough qubits for comparison!'
    
    number_bits = number_bits.zfill(n)

    qubits = QuantumRegister(n + 1)
    circuit = QuantumCircuit(qubits)

    input = qubits[0:n]
    result = qubits[n]

    if type == '!=' or type == '>=' or type == '>':
        circuit.x(result)
    
    actions[type]()
    
    return circuit
