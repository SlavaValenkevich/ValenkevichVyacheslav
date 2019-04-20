import random
import math

def is_prime(a):
    """
    Tests to see if a number is prime.

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
    pass


def gcd(A, B):
    """
    Euclid's algorithm for determining the greatest common divisor.

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
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.

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
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
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
