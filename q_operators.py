from qiskit import QuantumRegister, QuantumCircuit


def diffusion_constructor(n):

    assert n > 1, 'Argument n should be > 1.'
    
    qubits = QuantumRegister(n)
    circuit = QuantumCircuit(qubits)

    circuit.h(qubits)
    circuit.x(qubits)
    circuit.h(qubits[-1])
    
    length = len(qubits)
    
    if length > 3:
        circuit.mcx(qubits[0:-1], qubits[-1])
    elif length == 3:
        circuit.toffoli(*qubits[0:-1], qubits[2])
    elif length == 2:
        circuit.cx(qubits[0], qubits[1])
    
    circuit.h(qubits[-1])
    circuit.x(qubits)
    circuit.h(qubits)

    return circuit


def controlled_diffusion_constructor(q, c):

    '''
    Requires n + c qubits:
    - q — input qubits
    - c — controll qubits
    '''

    assert q > 1, 'Argument q should be > 1.'
    
    qubits = QuantumRegister(q + c)
    circuit = QuantumCircuit(qubits)

    if c > 0:
        control = qubits[q:]

    input = qubits[0:q]
    circuit.h(input)
    circuit.x(input)
    circuit.h(input[-1])
    
    length = len(input)
    
    if length == 2:
        if c > 0:
            circuit.mcx([*control, input[0]], input[1])
        else:
            circuit.cx(input[0], input[1])
        
    elif length >= 3:
        if c > 0:
            circuit.mcx([*control, *input[0:-1]], input[-1])
        else:
            circuit.mcx(input[0:-1], input[-1])
    
    circuit.h(input[-1])
    circuit.x(input)
    circuit.h(input)

    return circuit


def test_oracle_answers(n, q):
    N = 2 ** q
    x = N - n  # if n > N/2 else n
    X = []
    for i in range(x, N):
        if i >= N / 2:
            X.append(str(bin(i))[2:][::-1])
        else:
            X.append(str(bin(i))[2:].zfill(q)[::-1])
    return list(reversed(X))


def test_oracle_constructor(extra_arguments, inverted=False):

    '''
    Requires q qubits:
    - q — input qubits prepared with H gates
    '''

    # n — number of good answers
    # q — number of qubits
    
    n, q = extra_arguments
    
    qubits = QuantumRegister(q)
    circuit = QuantumCircuit(qubits)

    array = []
    x_close = []

    def crt(circuit, q_reg, n, array):
        q = len(q_reg)
        if n == 0:
            return array
        if n == 1:
            for e in q_reg:
                array.append(e)
            return array
        lim = 2 ** (q - 1)
        if n <= lim:
            array.append(q_reg[0])    
            n = n % lim
            array = crt(circuit, q_reg[1:], n, array)
        else:
            array.append(q_reg[0])
            circuit.h(array[-1])
            if len(array) > 1:
                circuit.mcx(array[0:-1], array[-1])
            else:
                circuit.x(array[0])
            circuit.h(array[-1])
            circuit.x(q_reg[0])
            x_close.append(q_reg[0])
            n = n % lim
            array = crt(circuit, q_reg[1:], n, array)
        return array

    array = crt(circuit, qubits, n, array)

    if len(array) == 1:
        circuit.h(array[0])
        circuit.x(array[0])
        circuit.h(array[0])
    elif len(array) > 1:
        circuit.h(array[-1])
        circuit.mcx(array[0:-1], array[-1])
        circuit.h(array[-1])

    if len(x_close) > 0:
        circuit.x(x_close)

    return circuit
