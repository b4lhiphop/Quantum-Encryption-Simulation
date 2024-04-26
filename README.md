# Quantum-Encryption-Simulation
Quantum Key Distribution (QKD) Simulator
This Quantum Key Distribution (QKD) Simulator is a Python program that demonstrates the BB84 protocol for secure key exchange. It simulates the process of key generation, transmission, and secure communication between Alice and Bob.

Features:
Alice creates a random key and encodes it onto qubits using two different bases.
Bob receives the qubits and randomly selects bases to measure them.
Alice and Bob compare bases to ensure the integrity of the key.
If the bases match, Alice and Bob obtain a secure shared key for encryption and decryption.
Encryption and decryption of a message using the generated secure key.
Technologies Used:
Python
Cirq (for quantum circuit simulation)
How to Use:
Run the program.
Follow the instructions to simulate the BB84 protocol between Alice and Bob.
After key generation, use the generated key to encrypt and decrypt a message.
