import sys
import numpy as np
import random
import cirq
from random import choices
import string

BASES = ['+', '-']
BITS = ['0', '1']
length = 10
encode_gates = {0: cirq.I, 1: cirq.X}
basis_gates = {'Z': cirq.I, 'X': cirq.H}
qubits = cirq.NamedQubit.range(length, prefix='q')
chars = ""+string.punctuation + string.ascii_letters + string.digits
chars = list(chars)
#ALICE CREATION
def make_alice_key(length=10):
    alice_key = choices([0, 1], k=length)
    bases = choices(['Z', 'X'], k=length)
    return alice_key, bases

def create_alice_circuit(alice_key,alice_bases):
    alice_circuit = cirq.Circuit()

    for bit in range(length):
        encode_value = alice_key[bit]
        encode_gate = encode_gates[encode_value]

        basis_value = alice_bases[bit]
        basis_gate = basis_gates[basis_value]

        qubit = qubits[bit]
        alice_circuit.append(encode_gate(qubit))
        alice_circuit.append(basis_gate(qubit))
    
    return alice_circuit
#BOB CREATION
def bases():
    bob_bases = []
    for i in range(length):
        while True:
            choice = input(f"Choose a base for qubit {i+1} (X or Z): ")
            if choice.lower() in ['x', 'z']:
                bob_bases.append(choice.upper())  # Convert to uppercase
                break
            else:
                print("Invalid input. Please enter either X or Z.")
    return bob_bases

def circuit(bob_bases):
    bob_circuit = cirq.Circuit()
    for bit in range(length):

        basis_value = bob_bases[bit]
        basis_gate = basis_gates[basis_value]

        qubit = qubits[bit]
        bob_circuit.append(basis_gate(qubit))
    
    return bob_circuit
#BOB MEASURES AND CREATES INITIAL KEY
def bob_measure(bob_circuit):
    bob_circuit.append(cirq.measure(qubits, key='bob key'))
    return bob_circuit

def bob_initial_key(alice_circuit, bob_circuit):
    bb84_circuit = alice_circuit + bob_circuit

    sim = cirq.Simulator()
    results = sim.run(bb84_circuit)
    bob_key = results.measurements['bob key'][0]
    return bob_key
#BOB AND ALICE COMPARE BASES TO MAKE SURE THEY MATCH
def compare_bases(alice_bases, alice_key, bob_key, bob_bases):
    final_alice_key = []
    final_bob_key = []
    corrupted = False
    for bit in range(length):
        if alice_bases[bit] == bob_bases[bit]:
            final_alice_key.append(alice_key[bit])
            final_bob_key.append(bob_key[bit])
        else:
            corrupted = True
        
    
    return final_alice_key, final_bob_key, corrupted

def compare_bits(final_alice_key, final_bob_key):
    num_bits_to_compare = int(len(final_alice_key) * .5)
    if final_alice_key[0:num_bits_to_compare] == final_bob_key[0:num_bits_to_compare]:
        final_alice_key = final_alice_key[num_bits_to_compare:]
        final_bob_key = final_bob_key[num_bits_to_compare:]
        con = True
    else:
        con = False
    return con

def recieve(answer):
    if answer.lower() in ["r", "yes", "y"]:
        decision = True
    else:
        decision = False
    return decision

def again(answer):
    if answer.lower() in ["yes", "y"]:
        decision = True
    else:
        decision = False
    return decision

def survey():
    survey = input("Would you like to take our survey to evaluate your experience? ")
    if survey.lower() in ['yes', 'y', 'yessir']:
        question1 = input("Do you believe this experience helped advance your knowledge on the QKD process? (y for yes, n for no) ")
        if question1.lower() in ['n', 'no']:
            anything = input("I am sorry to hear that. Is there anything we could do to make your experience better? ")
            print("Thanks for your input. We will take that into consideration as we work on improving our product.")
    print("Ok, thanks for playing! Bye.")

def print_bases(bases):
    num = 1

    for b in bases:
        print(f"base {num}: {b}", end=",")
        num += 1

def messages():
    messages = [
        "You are great!",
        "You are amazing!",
        "You are awesome!",
        "You are fantastic!",
        "You are incredible!",
        "You are outstanding!",
        "You are exceptional!",
        "You are phenomenal!",
        "You are superb!",
        "You are extraordinary!",
        "You are outstanding!",
        "You are remarkable!",
        "You are terrific!",
        "You are wonderful!",
        "You are splendid!"
    ]
    message = random.choice(messages)
    return message
#ENCRYPTION/DECRYPTION
def encrypt(message, key):
    encrypted_message = ""
    key_length = len(key)
    for i in range(len(message)):
        char = message[i]
        if char.isalpha():
            shift = int(key[i % key_length])
            encrypted_char = chr((ord(char) - 65 + shift) % 26 + 65) if char.isupper() else chr((ord(char) - 97 + shift) % 26 + 97)
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message

def decrypt(encrypted_message, key):
    decrypted_message = ""
    key_length = len(key)
    for i in range(len(encrypted_message)): 
        char = encrypted_message[i]
        if char.isalpha():
            shift = int(key[i % key_length])
            decrypted_char = chr((ord(char) - 65 - shift) % 26 + 65) if char.isupper() else chr((ord(char) - 97 - shift) % 26 + 97)
            decrypted_message += decrypted_char
        else:
            decrypted_message += char
    return decrypted_message
def repeat_key(key, length):
    return [key] * length

    


def part1():
    #ALICE PREP
    alice_key, alice_bases = make_alice_key(10) # Alice makes her key
    alice_circuit = create_alice_circuit(alice_key,alice_bases) #Alice Makes Her qubits
    #AlICE SENDS QUBITS TO BOB
    print("Alice has prepared her qubits and sends them to Bob.")
    answer = input("Bob, do you want to receive the qubits? (Type 'R' to receive, or 'N' to not receive): ")
    if recieve(answer) == False:
        print("You have chosen not to receive the qubits. The simulation ends here.")
        survey()
        sys.exit()
    #BOB RECIEVES CUBITS, and then chooses thier bases
    print("You have received the qubits. Now, it's your turn to choose bases.")
    print("For each qubit, choose a measurement basis (X or Z):")
    bob_bases = bases()
    print(f"Your bases are: {bob_bases}")#PRINTS BOB BASES

    bob_circuit = circuit(bob_bases)
    bob_circuit = bob_measure(bob_circuit)
    print(f"You measured your circuit which gives you {bob_circuit}")
    bob_key = bob_initial_key(alice_circuit, bob_circuit)

    final_alice_key, final_bob_key,corrupted = compare_bases(alice_bases, alice_key, bob_key, bob_bases)
    print("You then compare your qubits with alice's to see if they match")
    if corrupted:
        print("Eve was hard at work, but with our great detection method, we were able to remove all of her corrupted qubits from the final key.")
    else:
        print("Eve was thankfully not at work today, but even if she was, we would have been able to detect her and make a new key without her influence.")       
    secure_final_key = final_alice_key 
    print(f"Our secured final key is {secure_final_key}")
    print(f"Alice: {final_alice_key}\n Bob: {final_bob_key}")
    con = compare_bits(final_alice_key, final_bob_key)
    

    if con:
        print("Alice and Bob's keys match. They can use them for encryption and decryption.")
        secure_final_key = final_alice_key
        return secure_final_key
    else:
        print("Alice and Bob's keys do not match. The simulation ends here.")
        survey()
        sys.exit()


def part2(message, key):
    chars = ""+string.punctuation + string.ascii_letters + string.digits
    chars = list(chars)
    key = repeat_key(key,len(message))
    encrypted_message = encrypt(message,key)
    print(f"Encrypted Message:{encrypted_message}")
    decrypted_message = decrypt(encrypted_message, key)
    print(f"Decrypted Message:{decrypted_message}")
    random.shuffle(key)



print("Hello user, Welcome to the Quantum Key Distribution Simulator. Today you will experience the wonderful process of QKD in real-time. You will be playing the role of Bob in both receiving the key and using it to encrypt and decrypt the message.")
# alice_secret_key, alice_bases = prepare_qubits(10)  # Alice's secret key and bases
message = messages()
key = part1()
new_key = ''
for i in key:
    new_key = new_key + str(i)
key = new_key
# encrypted_message = encrypt(message,key)
# decrypted_message = decrypt(encrypted_message,key)
# print(encrypted_message)
# print(decrypted_message)
# print("The next step is decryption")
# print(f"Are encrypted message is {encrypted_message}")
# print(f"Are decrypted message is {encrypted_message}")
part2(message,key)

