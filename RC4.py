import fileinput

# ---- LECTURA DE DATOS
entrada = []
S = list(range(256))

for line in fileinput.input(): entrada.append(line.rstrip())

plain_k = entrada[0]
plain_t = entrada[1]

# ---- PROCESO DE KSA
def KSA(key):
    j = 0
    key_length = len(key)
    for i in range(0, 256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

# ---- PROCESO DE PRGA
def PRGA(S):
    global plain_t
    i, j = 0, 0
    result = []
    for k in range(len(plain_t)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(K)
    return result

def E(key, plainText):
    e_msg = []
    key = [ord(i) for i in key]
    S = KSA(key)
    K = PRGA(S)
    for i, k in zip(plainText, K):
        hex_val = "%02X" % (ord(i) ^ k)
        e_msg.append(hex_val)
    return "".join(e_msg)

print(E(plain_k, plain_t))
