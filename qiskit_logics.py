from qiskit import QuantumRegister, QuantumCircuit


def logic_operation(n, operation):

    """
    Available operation types: "and", "or" and "xor".
    Required (n + 1) qubits:
    -- [:n] — input qubits
    -- [n] — result qubit
    """
    
    qr = QuantumRegister(n + 1)
    qc = QuantumCircuit(qr)

    xs = qr[:n]
    result = qr[-1]

    def __and():
        qc.mcx(xs, result)
    
    def __or():
        qc.x([*xs, result])
        qc.mcx(xs, result)
        qc.x(xs)

    def __xor():
        qc.x([*xs, result])
        qc.mcx(xs, result)
        qc.x(xs)
        qc.mcx(xs, result)

    actions = {
        'and': __and,
        'or': __or,
        'xor': __xor,
    }

    actions[operation]()

    return qc
