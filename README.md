# Qiskit extensions

Репозиторий **qiskit_extensions** содержит набор «авторских» 
расширений для библиотеки **qiskit**.

> **Qiskit** — библиотека для квантовых вычислений на языке **Python** от компании **IBM**.

Для использования библиотеки в собственном проекте необходимо выполнить несколько шагов.

Предварительные условия:

1. В системе установлен язык **Python**.
2. Установлен менеджер пакетов **pip** для языка **Python**.
3. Установлена библиотека **httpimport** для удаленного импорта модулей в проекты на языке **Python**.
4. Установлена библиотека **qiskit** для квантовых вычислений на языке **Python**.

Для подключения модулей из репозитория необходимо в файле проекта вставить следующий код:

```python
from httpimport import remote_repo

with remote_repo(['qiskit_logics', 'qiskit_arithmetics'], 'https://raw.githubusercontent.com/kochelev/qiskit_extensions/master/'):
    import qiskit_logics as ql
    import qiskit_arithmetics as qa
```

Далее вы можете использовать ресурсы подключенных модулей как обычно:

```python
import numpy as np
from qiskit import execute
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit_aer import Aer

qr = QuantumRegister(4)
qc = QuantumCircuit(qr)

xs = qr[:-1]
result = qr[-1]

qc.append(ql.logic_operation(3, 'xor'), [*xs, result])
```
