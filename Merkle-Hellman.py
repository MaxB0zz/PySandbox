from random import randint
from string import printable
import secrets
import datetime

message_size = 10000000
message = secrets.token_hex(message_size // 2)
charset = list(map(str, printable))


def pgcd(n, m):
    while m != 0:
        n, m = m, n % m
    return n


# On commence part generer une clé privée pour un message de n taille
def generate_private_key(n):
    # on creer un sac d'elements super-croissants
    sac_super_croissant = []
    somme_des_elements_anterieurs = 0
    for index in range(n):
        incrementation_aleatoire = randint(1, 10)
        sac_super_croissant.append(somme_des_elements_anterieurs + incrementation_aleatoire)
        somme_des_elements_anterieurs += sac_super_croissant[index]

    # On genere un nombre plus grand que la somme des elements de notre liste
    N = randint(somme_des_elements_anterieurs + 1, 2 * somme_des_elements_anterieurs)

    # Ensuite on recherche un entier A tel que le PGCD(A, N) = 1
    A = randint(0, somme_des_elements_anterieurs)
    while pgcd(A, N) != 1:
        A += 1
    return N, A, sac_super_croissant


# Maitenant on peut generer la clé publique a partir de la clé privée
def generate_public_key(N, A, sac):
    new_sac = sac.copy()
    for index in range(len(new_sac)):
        new_sac[index] = (sac[index] * A) % N
    return new_sac


def encrypt(m, key):
    secret_message = 0
    # On a juste besoin de sommer les elements de la clé
    for index in range(len(m)):
        secret_message += int(m[index]) * key[index]
    return secret_message


def decrypt(c, N, A, sac, size):
    # pow(A, -1, N) = A^-1
    decrypted = size * [0]
    p = (c * pow(A, -1, N)) % N
    n = len(sac) - 1
    while p > 0 and n >= 0:
        if p >= sac[n]:
            decrypted[n] = 1
            p -= sac[n]
        n -= 1
    return "".join([str(elem) for elem in decrypted])


def string_to_binary(s):
    b = []
    for c in s:
        b.append(format(ord(c), 'b'))
    return b


def same_list(a, b):
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


if __name__ == "__main__":
    print("message: ", message)
    print("size of the key : ", len(message))
    binary_message = string_to_binary(message)
    print("Message binaire : ", binary_message[0], ", ..., ", binary_message[-1])
    print("=========================================================")

    private_key_generation = datetime.datetime.now()
    N, A, sac = generate_private_key(8)
    private_key_generation = private_key_generation - datetime.datetime.now()
    print("Cle privée : ", sac[0], ", ..., ", sac[-1])
    print("DURATION : ", str(private_key_generation.total_seconds() * -1), "s")
    print("=========================================================")

    public_key_generation = datetime.datetime.now()
    c = generate_public_key(N, A, sac)
    public_key_generation = public_key_generation - datetime.datetime.now()
    print("Cle publique : ", c[0], ", ..., ", c[-1])
    print("DURATION : ", str(public_key_generation.total_seconds() * -1), "s")
    print("=========================================================")

    crypting_time = datetime.datetime.now()
    crypted_message = []
    for bin in binary_message:
        crypted_character = encrypt(bin, c)
        crypted_message.append(crypted_character)
    crypting_time = crypting_time - datetime.datetime.now()
    print("Message chiffré : ", crypted_message[0], ", ..., ", crypted_message[-1])
    print("DURATION : ", str(crypting_time.total_seconds() * -1), "s")
    print("=========================================================")

    decrypting_time = datetime.datetime.now()
    decrypted_message = []
    for index in range(len(crypted_message)):
        size = len(binary_message[index])
        decrypted_message.append(decrypt(crypted_message[index], N, A, sac, size))
    decrypting_time = decrypting_time - datetime.datetime.now()
    print("Message dechiffré : ", decrypted_message[0], ", ..., ", decrypted_message[-1])
    print("Is Same Message : ", same_list(decrypted_message, binary_message))
    print("DURATION : ", str(decrypting_time.total_seconds() * -1), "s")
    print("=========================================================")
