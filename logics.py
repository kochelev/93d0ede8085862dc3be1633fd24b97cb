from qiskit import QuantumRegister, QuantumCircuit


def logic_operation(n, operation):

    """
    Available operation types: "and", "or" and "xor".
    Required (n + 1) qubits:
    -- [:n] — input
    -- [n] - result
    """
    
    qr = QuantumRegister(n + 1)
    qc = QuantumCircuit(qr)

    X = qr[:n]
    result = qr[-1]

    def __and():
        qc.mcx(X, result)
    
    def __or():
        qc.x([*X, result])
        qc.mcx(X, result)
        qc.x(X)

    def __xor():
        qc.x([*X, result])
        qc.mcx(X, result)
        qc.x(X)
        qc.mcx(X, result)

    actions = {
        'and': __and,
        'or': __or,
        'xor': __xor,
    }

    actions[operation]()

    return qc
