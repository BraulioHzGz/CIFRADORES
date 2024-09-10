import fileinput
import math

dictionary = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9,
              "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18,
              "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}

inverse_dictionary = {v: k for k, v in dictionary.items()}
mod = len(dictionary)

# ---- LECTURA DE DATOS
entrada = []
array_key = []
array_msg = []
n = 1
index = 0

for line in fileinput.input():
    entrada.append(line.rstrip())

mode = entrada[0]
key = entrada[2]
mensaje = entrada[1]

# ---- RELLENADO DE CARACTERES EN MATRICES DE n x n
while len(key) > (n * n):
    n += 1

array_key = [[0 for _ in range(n)] for _ in range(n)]

for j in range(n):
    for i in range(n):
        if index < len(key): array_key[i][j] = dictionary[key[index]]
        else: array_key[i][j] = dictionary["X"]
        index += 1

# ---- PROCESO DE CIFRADO
def matrix_multiply(key, text_blocks):
    rows_key, cols_key = len(key), len(key[0])
    result = ""

    for text in text_blocks:
        block_result = [0 for _ in range(rows_key)]
        for i in range(rows_key):
            for j in range(cols_key):
                block_result[i] = (block_result[i] + key[i][j] * text[j]) % mod
        result += ''.join(inverse_dictionary[val] for val in block_result)
    return result


# ---- PROCESO DE DESCIFRADO
def subMatrix(array, i, j):
    return [row[:j] + row[j + 1:] for row in array[:i] + array[i + 1:]]

def det(array):
    _det = 0
    n = len(array)
    if n == 1: _det = array[0][0]
    elif n == 2: _det = array[0][0] * array[1][1] - array[0][1] * array[1][0]
    else:
        for i in range(len(array)):
            _det += ((-1) ** i) * array[0][i] * det(subMatrix(array, 0, i))
    return _det

def modular_det(value):
    value = value % mod
    for i in range(1, mod):
        if (value * i) % mod == 1:
            return i
    return None

def adj_matrix(array):
    global n
    cofactor = [[0] * n for _ in range(n)]
    transpose = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            get_minor = subMatrix(array, i, j)
            cofactor[i][j] = (((-1) ** (i + j)) * det(get_minor)) % mod
            transpose[j][i] = cofactor[i][j] % mod
    return transpose

def inverse_array(array):
    global n
    _det = modular_det(det(array))
    if _det is None:
        print("No tiene módulo")
        return array
    aux = adj_matrix(array)
    rows, cols = len(array), len(array[0])
    inverse_array = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            inverse_array[i][j] = (_det * aux[i][j]) % mod
    return inverse_array

def fill_msg(index, n):
    global mensaje, mode

    array_msg = []
    while index < len(mensaje):
        aux = []
        for _ in range(n):
            if(index < len(mensaje)): aux.append(dictionary[mensaje[index]])
            else: aux.append(dictionary["X"])
            index += 1
        array_msg.append(aux)
    if mode == 'C':
        msg = matrix_multiply(array_key, array_msg)
    elif mode == 'D':
        msg = matrix_multiply(inverse_array(array_key), array_msg)
    return msg

match mode:
    case 'C':
        print(fill_msg(0, n))
    case 'D':
        print(fill_msg(0, n))
