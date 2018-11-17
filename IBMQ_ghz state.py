# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 10:26:01 2018

@author: sajid Ullah
"""

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, execute, IBMQ
from qiskit.backends.ibmq import least_busy


q=QuantumRegister(5,"q")

c=ClassicalRegister(5, "c")

qc=QuantumCircuit(q, c, name='ghz')

#create a GHZ state
qc.h(q[0])
for i in range(4):
    qc.cx(q[i], q[i+1])
    # produce barrier
qc.barrier()

for i in range(5):
    qc.measure(q[i], c[i]) 
    
#simulating the program
try:
    IBMQ.loadaccounts()
except:
    print("No account on IBMQ server found")   
    
#simulation
sim_backend=Aer.get_backend('qasm_simulator')
job=execute(qc, sim_backend, shots=1024)
result=job.result()
print('qasm simulator')
print(result)
print(result.get_counts(qc))

# Second version: real device
least_busy_device = least_busy(IBMQ.backends(simulator=False,
                                             filters=lambda x: x.configuration()['n_qubits'] > 4))
print("Running on current least busy device: ", least_busy_device)
job = execute(qc, least_busy_device, shots=1024)
result = job.result()
print(result)
print(result.get_counts(qc))
