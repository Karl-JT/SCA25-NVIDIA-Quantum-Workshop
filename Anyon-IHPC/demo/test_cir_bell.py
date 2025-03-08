import cudaq
import numpy as np

bell_pair = cudaq.make_kernel()
qubits = bell_pair.qalloc(2)
bell_pair.h(qubits[0])         
bell_pair.cx(qubits[0], qubits[1])  
bell_pair.mz(qubits[0])
bell_pair.mz(qubits[1])

print(cudaq.draw(bell_pair))

openqasm_code=cudaq.translate(bell_pair, format="openqasm2")
print(openqasm_code)

cudaq.set_target("qpp-cpu")

sample_result = cudaq.sample(bell_pair,shots_count=1000)
print(sample_result)
