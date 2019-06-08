# - * -coding: utf - 8 - * -

import random
import math


def is_prime(a):

    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """

    # функция на проверку простого числа
    if a == 0:
    	return False
    elif a > 0 and a <= 3:
        return True
    elif a > 3:
        # проверка на простоту
        for i in range(2, int(math.sqrt(a))+1):
            # перебор чисел для проверки
            if (a % i == 0):
                # проверка каждого из них, если а делится нацело не только на себя и 1, то число не простое
                return False
            else:
                return True
    elif a == 1:
        return ("You input 1")
    else:
        return ('The number is negative')


def gcd(A, B):
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """

    mod = A % B
    divs = [A // B]
    while mod != 0:
        A = B
        B = mod
        mod = A % B
        divs.append(A // B)
        return mod


def multiplicative_inverse(e, phi):

    """
    >>> multiplicative_inverse(7, 40)
    23
    """

    A = phi

    # From up to down
    mod = phi % e
    divs = [phi // e]
    while mod != 0:
        phi = e
        e = mod
        mod = phi % e
        divs.append(phi // e)
        # From down to up
        x = 0
        y = 1
        for i in range(len(divs) - 1, 0, -1):
            x_prev = y
            y_prev = x - y * divs[i-1]

            x = x_prev
            y = y_prev
    return y % A


def generate_keypair(p, q):
    if not(is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    phi = (p - 1) * (q - 1)

    # Выбрать целое число е так, чтобы e и phi(n) были взаимнопростыми
    e = random.randrange(1, phi)
    is_prime(e)

    # Использовать алгоритм евклида для проверки взаимной простоты чисел e и phi(n)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Использовать расширенный алгорит Евклида для генерации приватного ключа 
    d = multiplicative_inverse(phi, e)

    # Возвращется публичная иприватная пара ключей 
    # Публичный ключ (e, n) и приватный ключ (d, n)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    # Распаковать ключи по компонентам 
    key, n = pk
    # Конвертировать каждый символ исходного сообщения в число на основе символа используя a ^ b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Вернуть массив байт
    return cipher


def decrypt(pk, ciphertext):
    # Распаковать ключи по компонентам
    key, n = pk
    # Сгенерировать исходное сообщение основываясь на зашифрованном сообщения и ключе используя a ^ b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Вернуть массив байт в строке
    return ''.join(plain)


if __name__ == '__main__':
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
