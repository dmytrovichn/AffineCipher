import os
from random import randint

import numpy as np
from sympy import Matrix


class Text:

    @staticmethod
    def convert(text):
        res = [ord(i) - 32 for i in text]
        return np.array(res)


class Key:

    @classmethod
    def validate(cls, a, s):
        for i in a:
            for j in i:
                if 0 > j > 94:
                    return False

        for i in s:
            if 0 > i > 94:
                return False

        k_a = np.array(a)
        if cls.gcd(int(np.linalg.det(k_a)), 95) == 1:
            return True

        return False

    @classmethod
    def gcd(cls, x, y):
        while y:
            x, y = y, x % y

        return x

    @classmethod
    def create(cls, k):
        print('Create A')
        try:
            a = []
            for i in range(k):
                row = []
                for j in range(k):
                    value = int(input(f'[{i}][{j}] = '))
                    row.append(value)
                a.append(row)
        except Exception as e:
            print(e)
            return

        print('Create S')
        try:
           s = []
           for i in range(k):
               value = int(input(f'[{i}][0] = '))
               s.append(value)
        except Exception as e:
            print(e)
            return

        if cls.validate(a, s):
            return a, s

        print('KEY IS NOT CORRECT.')

    @classmethod
    def generate(cls, k):
        while True:
            a = [[randint(0, 94) for _ in range(k)] for _ in range(k)]
            s = [randint(0, 94) for _ in range(k)]
            if cls.validate(a, s):
                break

        return a, s

    @classmethod
    def save(cls, a, s, file_name):
        output = ''
        for row in a:
            output += ' '.join(str(x) for x in row) + '\n'

        output += '\n'

        output += ' '.join(str(x) for x in s)

        with open(f'{file_name}.txt', 'w', encoding='utf-8') as g:
            g.write(output)
        print('Key was saved successfully.')

    @classmethod
    def load(cls, file_name):
        try:
            with open(f'{file_name}.txt', 'r', encoding='utf-8') as f:
                output = f.readlines()

            a = []
            for line in output:
                if not line.strip():
                    break
                a.append([int(i) for i in line.split()])

            s = [int(i) for i in output[-1].split()]
            if cls.validate(a, s):
                return a, s

            raise ValueError('The key is incorrect')
        except (IOError, FileExistsError, FileNotFoundError, ValueError) as e:
            print(f'Error: {e}')

    @classmethod
    def inverse(cls, a):
        a_inv = Matrix(a).inv_mod(95)
        return np.array(a_inv.tolist())


class Affine:

    @classmethod
    def encryption(cls, a, s, file_name):
        if os.path.exists(f'{file_name}_encrypted.txt'):
            os.remove(f'{file_name}_encrypted.txt')

        with open(f'{file_name}.txt', 'r', encoding='utf-8') as f:
            while True:
                    output = ''
                    k_len = len(a[0])
                    text = f.read(k_len)
                    if text == '':
                        print('File was successfully encrypted.')
                        break
                    text = Text.convert(text)
                    while len(text) != len(s):
                        text = np.append(text, 0)
                    encrypted = np.add(
                        np.array(s),
                        np.dot(a, text)
                    )
                    for i in encrypted:
                        output += chr(i % 95 + 32)
                    with open(f'{file_name}_encrypted.txt', 'a') as g:
                        g.write(output)

    @classmethod
    def decryption(cls, a, s, file_name):
        if os.path.exists(f'{file_name.split("_")[0]}_decrypted.txt'):
            os.remove(f'{file_name.split("_")[0]}_decrypted.txt')

        with open(f'{file_name}.txt', 'r') as f:
            while True:
                output = ''
                k_len = len(a[0])
                text = f.read(k_len)
                if not text:
                    print('File was successfully decrypted.')
                    break
                text = Text.convert(text)
                decrypted = np.add(
                    np.dot(Key.inverse(a), text),
                    np.dot(-1 * Key.inverse(a), s)
                )
                for i in decrypted:
                    output += chr(i % 95 + 32)
                with open(f'{file_name.split("_")[0]}_decrypted.txt', 'a') as g:
                    g.write(output)
