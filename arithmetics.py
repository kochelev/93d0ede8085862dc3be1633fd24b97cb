from qiskit import QuantumRegister, QuantumCircuit


# COMPARISON


# Variable vs. variable


def cmp_vv(vrb_1_ln, operation, vrb_2_ln):

    '''
    COMPARE VARIABLE AND VARIABLE
    Compares numbers stored in the qubits of input 1 and input 2.
    Operation types: "==", "!=", ">", ">=", "<", "<="
    Requires (vrb_1_ln + vrb_2_ln + 1) qubits:
    - vrb_1_ln — first input qubits
    - vrb_2_ln — second input qubits
    - 1 — qubit for the result
    '''
    
    def if_eq_vv(X_1, X_2):
    
        main, additional = (X_1, X_2) if vrb_1_ln >= vrb_2_ln else (X_2, X_1)

        qc.x(main)

        for i, a in enumerate(additional):
            qc.cx(a, main[i])

        qc.mcx(main, result)

        for i, a in enumerate(additional):
            qc.cx(a, main[i])

        qc.x(main)

        return qc

    def if_ls_vv(X_1, X_2):

        l = len(X_2) if len(X_2) < len(X_1) else len(X_1)
        
        shr_n_1, shr_n_2 = X_2[0:l], X_1[0:l]
        
        exq = []
        e = 0
        
        if len(X_2) > len(X_1):
            e = len(X_2) - len(X_1)
            exq = X_2[l:]
            for i in reversed(range(e)):
                qc.mcx([*exq[i:e]], result)
                qc.x(exq[i])
        elif len(X_1) > len(X_2):
            e = len(X_1) - len(X_2)
            exq = X_1[l:]
            qc.x(exq)

        for i in range(l):
            qc.mcx([*exq, shr_n_1[i]], shr_n_2[i])
            k = l - i
            for j in range(k):
                if j + i > l-2:
                    qc.mcx([*exq, shr_n_1[i], *shr_n_2[i : i + j + 2]], result)
                else:
                    qc.mcx([*exq, shr_n_1[i], *shr_n_2[i : i + j + 1]], shr_n_2[i + j + 1])
                    
        for i in reversed(range(l)):
            k = l - i
            for j in reversed(range(k)):
                if j + i > l-2:
                    pass
                else:
                    qc.mcx([*exq, shr_n_1[i], *shr_n_2[i : i + j + 1]], shr_n_2[i + j + 1])
                    
            qc.mcx([*exq, shr_n_1[i]], shr_n_2[i])

        if len(exq) > 0:
            qc.x(exq)

        return qc
    
    actions = {
        '==': if_eq_vv,
        '!=': if_eq_vv,
        '<': if_ls_vv,
        '<=': if_ls_vv,
        '>': if_ls_vv,
        '>=': if_ls_vv,
    }

    qr = QuantumRegister(vrb_1_ln + vrb_2_ln + 1)
    qc = QuantumCircuit(qr)

    X_1 = qr[:vrb_1_ln]
    X_2 = qr[vrb_1_ln:vrb_1_ln+vrb_2_ln]
    result = qr[-1]

    if operation == '!=' or operation == '>=' or operation == '<=':
        qc.x(result)
    
    if operation == '>' or operation == '<=':
        actions[operation](X_2, X_1)
    else:
        actions[operation](X_1, X_2)

    return qc


# Variable vs. constant


def cmp_vc(vrb_ln, operation, cnst):
    
    '''
    COMPARE VARIABLE AND CONSTANT
    Compares numbers stored in the qubits of input with exact digit.
    Operation types: "==", "!=", ">", ">=", "<", "<="
    Requires (vrb_ln + 1) qubits:
    - vrb_ln — input qubits
    - 1 — qubit for result
    '''

    def if_eq_vc(bits_cnst):

        bits_cnst = list(reversed(bits_cnst))

        if len(bits_cnst) > vrb_ln:
            return qc

        for i, bit in enumerate(bits_cnst):
            if bit == '0':
                qc.x(X[i])

        qc.mcx(X, result)

        for i, bit in enumerate(bits_cnst):
            if bit == '0':
                qc.x(X[i])

        return qc

    def if_ls_vc(bits_cnst):

        if len(bits_cnst) > vrb_ln:
            qc.x(result)
            return qc

        for i in range(vrb_ln):
            if bits_cnst[vrb_ln-i-1] == '1':
                qc.x(X[i:vrb_ln])
                break

        for i in range(vrb_ln):
            if bits_cnst[i] == '1':
                qc.mcx(X[vrb_ln-i-1:vrb_ln], result)
                qc.x(X[vrb_ln-i-1])

        for i in range(vrb_ln):
            if bits_cnst[vrb_ln-i-1] == '1':
                for j in range(i, vrb_ln):
                    if bits_cnst[vrb_ln-j-1] == '0':
                        qc.x(X[j])
                break

        return qc
    
    actions = {
        '==': if_eq_vc,
        '!=': if_eq_vc,
        '<': if_ls_vc,
        '<=': if_ls_vc,
        '>': if_ls_vc,
        '>=': if_ls_vc,
    }
    
    qr = QuantumRegister(vrb_ln + 1)
    qc = QuantumCircuit(qr)

    X = qr[0:vrb_ln]
    result = qr[-1]

    bits_cnst = str(bin(cnst))[2:].zfill(vrb_ln)

    if operation == '!=' or operation == '>=' or operation == '>':
        qc.x(result)
    
    actions[operation](bits_cnst)

    if operation == '<=' or operation == '>':
        actions['=='](bits_cnst)
    
    return qc


# UTILITY


def __propagate(n):
    
    qr = QuantumRegister(n)
    qc = QuantumCircuit(qr)

    for i in range(len(qr) - 1):
        source = []
        source += [qr[x] for x in range(i + 1)]
        if i != 0:
            qc.x(qr[i])
        qc.mcx(source, qr[i + 1])
    if n > 1:
        qc.x(qr[:-1])

    return qc


# ADDITION


# Addition. Variable with variable


def add_vv(vrb_1_ln, vrb_12_ln):

    '''
    Requires (vrb_1_ln + vrb_12_ln) qubits, where:
    - vrb_1_ln — number of qubits for variable 1
    - vrb_12_ln — number of qubits for variable 1 + variable 2, which required to store maximum possible result of addition operation
    '''

    qr = QuantumRegister(vrb_1_ln + vrb_12_ln)
    qc = QuantumCircuit(qr)

    vrb_1 = qr[0 : vrb_1_ln]
    vrb_12 = qr[vrb_1_ln : vrb_1_ln + vrb_12_ln]

    for i, x in enumerate(vrb_1):
        prp = __propagate(len(vrb_12[i:])).to_gate(label='+%d*x%d' % (2**i, i))
        c_prp = prp.control()
        qc.append(c_prp, [vrb_1[i], *vrb_12[i:]])    

    return qc


# Addition. Variable with constant


def add_vc(vrb_ln, cnst):

    '''
    Requires (vrb_ln = n + m) qubits, where:
    - n — number of qubits for variable
    - n + m — number of additional qubits, which required to store maximum possible result of addition operation (cnst + 2^n)
    '''

    qr = QuantumRegister(vrb_ln)
    qc = QuantumCircuit(qr)

    bits_cnst = list(reversed(bin(cnst)[2:].zfill(vrb_ln)))

    for i, bit in enumerate(bits_cnst):
        if bit == '1':
            qc.append(__propagate(len(qr[i:])).to_gate(label='Pr.'), qr[i:])    

    return qc


# SUBTRACTION


# Subtraction. Variable with variable


def subtract_vv(vrb_1_ln, vrb_2_ln):

    '''
    Requires (vrb_1_ln + vrb_12_ln) qubits, where:
    - vrb_1_ln — number of qubits for variable 1
    - vrb_12_ln — number of qubits for variable 1 + variable 2, which required to store maximum possible result of addition operation
    '''

    qr = QuantumRegister(vrb_1_ln + vrb_2_ln)
    qc = QuantumCircuit(qr)

    vrb_1 = qr[0 : vrb_1_ln]
    vrb_2 = qr[vrb_1_ln : vrb_1_ln + vrb_2_ln]

    qc.x(vrb_1)
    qc.append(__propagate(len(vrb_1)).to_gate(label='P'), vrb_1)

    qc.append(add_vv(len(vrb_2), len(vrb_1)).to_gate(label='V+V'), [*vrb_2, *vrb_1])

    qc.x(vrb_1)
    qc.append(__propagate(len(vrb_1)).to_gate(label='P'), vrb_1)


    return qc


# Subtraction. Variable with constant


def subtract_vc(vrb_ln, cnst):

    '''
    Requires (vrb_ln = n + m) qubits, where:
    - n — number of qubits for variable
    - n + m — number of additional qubits, which required to store maximum possible result of addition operation (cnst + 2^n)
    Constraints:
    - constant should be less than variable.
    '''

    qr = QuantumRegister(vrb_ln)
    qc = QuantumCircuit(qr)

    qc.x(qr)
    qc.append(__propagate(len(qr)).to_gate(label='P'), qr)
    qc.append(add_vc(len(qr), cnst).to_gate(label='+%d' % cnst), qr)
    qc.x(qr)
    qc.append(__propagate(len(qr)).to_gate(label='P'), qr)

    return qc


# MULTIPLICATION


# Multiplication. Variable with constant


def multiply_vc(vrb_ln, new_vrb_ln, cnst):

    '''
    Requires (vrb_ln + new_vrb_ln) qubits, where:
    - vrb_ln — number of qubits for variable
    - new_vrb_ln — number of qubits to store result, which requires number of qubits enought to store maximum possible result of multiplication operation (cnst * 2^vrb_ln)
    '''

    qr = QuantumRegister(vrb_ln + new_vrb_ln)
    qc = QuantumCircuit(qr)

    vrb = qr[0:vrb_ln]
    result = qr[vrb_ln:]

    bits_cnst = list(reversed(bin(cnst)[2:]))

    for i, x in enumerate(bits_cnst):
        if x == '1':
            for j, v in enumerate(vrb):
                prp = __propagate(len(result[i+j:])).to_gate(label='+1')
                c_prp = prp.control()
                qc.append(c_prp, [v, *result[i+j:]])

    return qc


# Multiplication. Variable with variable


def multiply_vv(vrb_1_ln, vrb_2_ln, rs_ln):

    '''
    jjjj
    '''

    qr = QuantumRegister(vrb_1_ln + vrb_2_ln + rs_ln)
    qc = QuantumCircuit(qr)

    vrb_1 = qr[0:vrb_1_ln]
    vrb_2 = qr[vrb_1_ln:vrb_1_ln+vrb_2_ln]
    result = qr[vrb_1_ln+vrb_2_ln:]

    for i, v1 in enumerate(vrb_1):
        for j, v2 in enumerate(vrb_2):
            prp = __propagate(len(result[i+j:])).to_gate(label='+1')
            c_prp = prp.control(num_ctrl_qubits=2)
            qc.append(c_prp, [v1, v2, *result[i+j:]])

    return qc


# DIVISION


# Division. Variable with constant


def divide_vc(vrb_ln, divider_ln, cnst):

    '''
    ddd
    '''

    qr = QuantumRegister(vrb_ln + divider_ln)
    qc = QuantumCircuit(qr)

    vrb = qr[0:vrb_ln]
    divider = qr[vrb_ln:]

    start_i = len(bin(cnst)[2:])

    for i in range(start_i - 1, vrb_ln):
        
        A_si = vrb_ln - i - 1
        A_ei = vrb_ln
        A_l = A_ei - A_si

        print(A_si, A_ei, A_l)
        
        cls = cmp_vc(A_l, '<', cnst).to_gate(label='<?')
        sbt = subtract_vc(A_l, cnst).to_gate(label='V-%d' % cnst)
        
        qc.x(divider[-i-1])

        qc.append(cls, [*vrb[A_si:], divider[-i-1]])
        c_sbt = sbt.control()
        qc.append(c_sbt, [divider[-i-1], *vrb[A_si:]])
        
    return qc


# Division. Variable with variable


def divide_vv(vrb_1_ln, vrb_2_ln, divider_ln):

    '''
    ooo
    '''

    qr = QuantumRegister(vrb_1_ln + vrb_2_ln + divider_ln)
    qc = QuantumCircuit(qr)

    vrb_1 = qr[:vrb_1_ln]
    vrb_2 = qr[vrb_1_ln:vrb_1_ln+vrb_2_ln]
    divider = qr[vrb_1_ln+vrb_2_ln:]

    if vrb_2_ln > 1:
        qc.x(vrb_2[1:])

    for i in range(vrb_1_ln):
        
        A_si = vrb_1_ln - i - 1
        A_ei = vrb_1_ln
        B_si = 0
        B_ei = i + 1 if vrb_2_ln > i + 1 else vrb_2_ln
        
        A_l = A_ei - A_si
        B_l = B_ei - B_si
        
        cls = cmp_vv(A_l, '<', B_l).to_gate(label='<?')
        sbt = subtract_vv(A_l, B_l).to_gate(label='V-V')
        
        if B_l < vrb_2_ln:
            cc_cls = cls.control(num_ctrl_qubits=vrb_2_ln-B_l)
            cc_sbt = sbt.control(num_ctrl_qubits=vrb_2_ln-B_l+1)
            qc.mcx(vrb_2[B_ei:], divider[-i-1])
            qc.append(cc_cls, [*vrb_2[B_ei:], *vrb_1[A_si:], *vrb_2[:B_ei], divider[-i-1]])
            qc.append(cc_sbt, [divider[-i-1], *vrb_2[B_ei:], *vrb_1[A_si:], *vrb_2[:B_ei]])
        else:
            qc.x(divider[-i-1])
            qc.append(cls, [*vrb_1[A_si:], *vrb_2[:B_ei], divider[-i-1]])
            c_sbt = sbt.control()
            qc.append(c_sbt, [divider[-i-1], *vrb_1[A_si:], *vrb_2])

        if B_l < vrb_2_ln:
            qc.x(vrb_2[B_ei])

    return qc

