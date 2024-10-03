import fileinput

# ---- LECTURA DE DATOS ----
entrada = []  # Sabr si se debe cifrar 'E' o descifrar 'D'
array_key = []  # Llave en formato binario
array_msg = []  # Mensaje en formato binario

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

for line in fileinput.input():
    entrada.append(line.rstrip())

def shift_left(pos, array):
    return array[pos:] + array[:pos]

def permutation_plain_text(array):
    # Permutación inicial: 1 5 2 0 3 7 4 6
    return [array[1], array[5], array[2], array[0], array[3], array[7], array[4], array[6]]

def inverse_permutation(array):
    # Permutación inversa: 3 0 2 4 6 1 7 5
    return [array[3], array[0], array[2], array[4], array[6], array[1], array[7], array[5]]

def permutation_key_text(array):
    # Permutación inicial de la llave: 2 4 1 6 3 9 0 8 7 5
    aux = [array[2], array[4], array[1], array[6], array[3], array[9], array[0], array[8], array[7], array[5]]
    return aux[:5], aux[5:]

def generate_subkeys(key):
    left, right = permutation_key_text(key)
    
    # Generación de K1
    left_shifted_1 = shift_left(1, left)
    right_shifted_1 = shift_left(1, right)
    total = left_shifted_1 + right_shifted_1
    K1 = [
        total[5], total[2], total[6], total[3], 
        total[7], total[4], total[9], total[8]
    ]
    
    # Generación de K2
    left_shifted_3 = shift_left(3, left)
    right_shifted_3 = shift_left(3, right)
    total = left_shifted_3 + right_shifted_3
    K2 = [
        total[5], total[2], total[6], total[3], 
        total[7], total[4], total[9], total[8]
    ]
    
    return K1, K2

def expand_and_permute(right):
    # Expansión y permutación de 4 bits a 8 bits: 3 0 1 2 1 2 3 0
    return [right[3], right[0], right[1], right[2], right[1], right[2], right[3], right[0]]

def sbox_lookup(bits, sbox):
    row = (bits[0] << 1) | bits[3]
    col = (bits[1] << 1) | bits[2]
    return [int(x) for x in format(sbox[row][col], '02b')]

def feistel_function(right, subkey):
    global S0, S1
    expanded = expand_and_permute(right)
    xor_out = [expanded[i] ^ subkey[i] for i in range(8)]
    left_ = xor_out[:4]
    right_ = xor_out[4:]
    sbox_output = sbox_lookup(left_, S0) + sbox_lookup(right_, S1)
    # Permutación P4: 1 3 2 0
    permuted = [sbox_output[1], sbox_output[3], sbox_output[2], sbox_output[0]]
    
    return permuted

def feistel_round(left, right, subkey):
    f_output = feistel_function(right, subkey)
    new_left = [left[i] ^ f_output[i] for i in range(4)]
    return new_left, right

def encrypt(plaintext, K1, K2):
    permuted = permutation_plain_text(plaintext)
    left, right = permuted[:4], permuted[4:]
    left, right = feistel_round(left, right, K1)
    
    left, right = right, left  # Intercambio
    left, right = feistel_round(left, right, K2)
    pre_output = left + right
    result = inverse_permutation(pre_output)
    return result

def decrypt(ciphertext, K1, K2):
    permuted = permutation_plain_text(ciphertext)
    left, right = permuted[:4], permuted[4:]
    left, right = feistel_round(left, right, K2)

    left, right = right, left  # Intercambio
    left, right = feistel_round(left, right, K1)
    pre_output = left + right
    result = inverse_permutation(pre_output)
    return result
    
modo = entrada[0]
key = [int(x) for x in entrada[1].strip()]
msg = [int(x) for x in entrada[2].strip()]

K1, K2 = generate_subkeys(key)

if modo == 'E':
    result = encrypt(msg, K1, K2)
else:
    result = decrypt(msg, K1, K2)

print(''.join(map(str, result)))
