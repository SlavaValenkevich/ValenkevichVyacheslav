def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext=""
    if shift <=26:
        shift=shift
    else:
        shift=shift%26 #остаток от деления
        print('Смещение=',shift)
    for i in plaintext:
        if (ord(i)>=65) and (ord(i)<=90): #ord  - достает код символа в ascii-таблице, здесь проверка на символы A-Z 
            if ((ord(i)+shift)>=65) and ((ord(i)+shift)<=90): #если символ со смещением укладывается в алфавит A-Z, то
                ciphertext=ciphertext+chr(ord(i)+shift) #добавляем этот символ в зашифрованную последовательность
            else:
                d=int(math.fabs(90-ord(i))) #иначе сделать "круг" 
                s=64+int(math.fabs((shift-d))) #вычислить новое смещение и прибавить
                ciphertext=ciphertext+chr(s) #добавить символ в последовательность
        if (ord(i)>=97) and (ord(i)<=122): #ord  - достает код символа в ascii-таблице, здесь проверка на символы a-z
            if ((ord(i)+shift)>=97) and ((ord(i)+shift)<=122): #если символ со смещением укладывается в алфавит a-z, то
                ciphertext=ciphertext+chr(ord(i)+shift) #добавить символ в последовательность
            else:
                d=int(math.fabs(122-ord(i))) #иначе делаем круг
                s=96+int(math.fabs((shift-d))) #вычисляем новое значение
                ciphertext=ciphertext+chr(s) #добавляем в последовательность
        if (ord(i)>=44) and (ord(i)<=57):
            ciphertext+=i
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    return plaintext
