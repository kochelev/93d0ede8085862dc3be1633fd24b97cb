import unittest
from qiskit import *
from qiskit_aer import *
from logics import logic_operation


def construct_circuit(operation, vrb_string):

    qr = QuantumRegister(4)
    cr = ClassicalRegister(1)
    qc = QuantumCircuit(qr, cr)

    xs = qr[:-1]
    result = qr[-1]

    bits_vrb = ''.join(reversed(vrb_string))

    for i, bit in enumerate(bits_vrb):
        if bit == '1':
            qc.x(xs[i])

    qc.append(logic_operation(len(xs), operation), [*xs, result])
    qc.measure(result, cr)

    simulator = Aer.get_backend('aer_simulator')
    result = execute(qc, backend=simulator, shots=100).result()
    counts = result.get_counts()

    return counts


class TestAND(unittest.TestCase):

    def test__positive_000(self):

        expected = {'0': 100}
        counts = construct_circuit('and', '000')
        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))

    def test__positive_010(self):

        expected = {'0': 100}
        counts = construct_circuit('and', '010')
        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))

    def test__positive_111(self):

        expected = {'1': 100}
        counts = construct_circuit('and', '111')
        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))


class TestOR(unittest.TestCase):

    def test__positive_000(self):

        expected = {'0': 100}
        counts = construct_circuit('or', '000')

        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))

    def test__positive_010(self):

        expected = {'1': 100}
        counts = construct_circuit('or', '010')
        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))

    def test__positive_111(self):

        expected = {'1': 100}
        counts = construct_circuit('or', '111')
        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))


class TestXOR(unittest.TestCase):

    def test__positive_000(self):

        expected = {'0': 100}
        counts = construct_circuit('xor', '000')
        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))

    def test__positive_010(self):

        expected = {'1': 100}
        counts = construct_circuit('xor', '010')

        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))

    def test__positive_111(self):

        expected = {'0': 100}
        counts = construct_circuit('xor', '111')
        self.assertDictEqual(counts, expected, 'Should be %s' % str(expected))

