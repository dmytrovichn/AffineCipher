import time

from affine import Key
from affine import Affine


while True:
    i = int(input('1. Encryption\n'
                  '2. Decryption\n'
                  '0. Exit\n'
                  '~ '))

    if i == 1:
        p = int(input('1. Create key\n'
                      '2. Import key\n'
                      '3. Generate key\n'
                      '0. Exit\n'
                      '~ '))
        if p == 1:
            while True:
                try:
                    k = int(input('Enter the key matrix size: '))
                    break
                except Exception as e:
                    print(e)
            a, s = Key.create(k)
            file_name = input('Enter file name to save key: ')
            Key.save(a, s, file_name)
        elif p == 2:
            file_name = input('Enter key file name: ')
            a, s = Key.load(file_name)
        elif p == 3:
            while True:
                try:
                    k = int(input('Enter the key matrix size: '))
                    break
                except Exception as e:
                    print(e)
            a, s = Key.generate(k)
            file_name = input('Enter file name to save key: ')
            Key.save(a, s, file_name)
        else:
            break
        file_name = input('Enter plain text file name: ')
        start_time = time.time()
        Affine.encryption(a, s, file_name)
        print(time.time() - start_time)
    elif i == 2:
        p = int(input('1. Import key\n'
                      '0. Exit\n'
                      '~ '))
        if p == 1:
            file_name = input('Enter key file name: ')
            a, s = Key.load(file_name)
        else:
            break
        file_name = input('Enter cipher text file name: ')
        start_time = time.time()
        Affine.decryption(a, s, file_name)
        print(time.time() - start_time)
    else:
        break

