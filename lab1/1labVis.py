import math


def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    if len(keyword) < len(plaintext):
        # целое число раз
        z = len(plaintext) // len(keyword)
        keyword *= z
        if len(plaintext) % len(keyword) != 0:
            d = len(plaintext) % len(keyword)
            for h in range(d):
                # добавление оставшихся символов ключа до длины текста
                keyword += keyword[h]
        while len(ciphertext) < len(plaintext):
            # дальше вычисление смещения для каждого символа относительно символа в ключе
            for i in range(len(plaintext)):
                if (ord(keyword[i]) >= 65) and (ord(keyword[i]) <= 90):
                    # если символ ключа A - Z, то смещение такое
                    shift = int(math.fabs(65 - ord(keyword[i])))
                elif(ord(keyword[i]) >= 97) and (ord(keyword[i]) <= 122):
                    shift = int(math.fabs(97 - ord(keyword[i])))
                    # если символ a - z, то смещение такое
                if (ord(plaintext[i]) >= 65) and (ord(plaintext[i]) <= 90):
                    # дальше логика точно как в шифровании цезаре
                    if ((ord(plaintext[i]) + shift) >= 65) and ((ord(plaintext[i]) + shift) <= 90):
                        ciphertext = ciphertext + chr(ord(plaintext[i]) + shift)
                    else:
                        d = int(math.fabs(90 - ord(plaintext[i])))
                        s = 64 + int(math.fabs((shift - d)))
                        ciphertext = ciphertext + chr(s)
                    shift = 0
                if (ord(plaintext[i]) >= 97) and (ord(plaintext[i]) <= 122):
                    if ((ord(plaintext[i]) + shift) >= 97) and ((ord(plaintext[i]) + shift) <= 122):
                        ciphertext = ciphertext + chr(ord(plaintext[i]) + shift)
                    else:
                        d = int(math.fabs(122 - ord(plaintext[i])))
                        s = 96 + int(math.fabs((shift - d)))
                        ciphertext = ciphertext + chr(s)
                    shift = 0
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    if len(keyword) < len(ciphertext):
        z = len(ciphertext) // len(keyword)
        # целое число раз
        keyword *= z
        if len(ciphertext) % len(keyword) != 0:
            d = len(ciphertext) % len(keyword)
            for h in range(d):
                keyword += keyword[h]
    while len(plaintext) < len(ciphertext):
        for i in range(len(ciphertext)):
            # дальше вычисление смещения для каждого символа относительно символа в ключе
            if (ord(keyword[i]) >= 65) and (ord(keyword[i]) <= 90):
                shift = int(math.fabs(65 - ord(keyword[i])))
                # если символ ключа A - Z, то смещение такое
            elif(ord(keyword[i]) >= 97) and (ord(keyword[i]) <= 122):
                shift = int(math.fabs(97 - ord(keyword[i])))
                # если символ a - z, то смещение такое
            if (ord(ciphertext[i]) >= 65) and (ord(ciphertext[i]) <= 90):
                # дальше логика точно как в дешифровке цезаре
                if ((ord(ciphertext[i]) - shift) >= 65) and ((ord(ciphertext[i]) - shift) <= 90):
                    plaintext = plaintext + chr(ord(ciphertext[i]) - shift)
                else:
                    d = int(math.fabs(65 - ord(ciphertext[i])))
                    s = 91 - int(math.fabs((shift - d)))
                    plaintext = plaintext + chr(s)
                shift = 0
            if (ord(ciphertext[i]) >= 97) and (ord(ciphertext[i]) <= 122):
                if ((ord(ciphertext[i]) - shift) >= 97) and ((ord(ciphertext[i]) - shift) <= 122):
                    plaintext = plaintext + chr(ord(ciphertext[i]) - shift)
                else:
                    d = int(math.fabs(ord(ciphertext[i]) - 97))
                    s = 123 - int(math.fabs((shift - d)))
                    plaintext = plaintext + chr(s)
                    shift = 0
    return plaintext
