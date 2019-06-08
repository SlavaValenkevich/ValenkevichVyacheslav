import math

def encrypt_caesar(plaintext,shift):
    """
    >>> encrypt_caesar("PYTHON",3)
    'SBWKRQ'
    >>> encrypt_caesar("python",3)
    'sbwkrq'
    >>> encrypt_caesar("Python3.6",3)
    'Sbwkrq3.6'
    >>> encrypt_caesar("",3)
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


def decrypt_caesar(ciphertext,shift):
    """
    >>> decrypt_caesar("SBWKRQ",3)
    'PYTHON'
    >>> decrypt_caesar("sbwkrq",3)
    'python'
    >>> decrypt_caesar("Sbwkrq3.6",3)
    'Python3.6'
    >>> decrypt_caesar("",3)
    ''
    """
    plaintext=""
    if shift <=26:
        shift=shift
    else:
        z=shift//26
        shift=shift-z*26
        print('Смещение=',shift)
    for i in ciphertext:
        if (ord(i)>=65) and (ord(i)<=90): 
            if ((ord(i)-shift)>=65) and ((ord(i)-shift)<=90): #то де самое, что и в верхней функции, только смещаем обратно 
                plaintext=plaintext+chr(ord(i)-shift)
            else:
                d=int(math.fabs(65-ord(i))) #сделали "круг" по алфавиту
                s=91-int(math.fabs((shift-d))) #вычислили новое смещение и вычли
                plaintext=plaintext+chr(s)
        if (ord(i)>=97) and (ord(i)<=122):
            if ((ord(i)-shift)>=97) and ((ord(i)-shift)<=122):
                plaintext=plaintext+chr(ord(i)-shift)
            else:
                d=int(math.fabs(ord(i)-97))
                s=123-int(math.fabs((shift-d)))
                plaintext=plaintext+chr(s)
        if (ord(i)>=44) and (ord(i)<=57):
            plaintext+=i   
    return plaintext

