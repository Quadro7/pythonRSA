import math, random
from constants import LOGO, ALPHABET


def toList(s: str) -> list:
    l = []
    for symbol in s:
        try:
            l.append(ALPHABET.index(symbol))
        except ValueError:
            print(f"Error: This symbol ({symbol}) is not present in the dictionary. Please use only the following symbols: " + "!@#$%^&*()-=_+[];',./?<>{}")
    return l


def toString(l: list) -> str:
    res = ""
    for n in l:
        res += ALPHABET[n % len(ALPHABET)]
    return res


def generatePrimeNumber(n):
    x = random.randrange(2**(n-1) + 1, 2**n - 1)
    while not millerRabinTest(x, 20):
        x = random.randrange(2**(n-1) + 1, 2**n - 1)
    return x


def millerRabinTest(candidate, numberOfTrials):
    evenComponent = candidate - 1
    maxDivisionsByTwo = 0
    while evenComponent % 2 == 0:
        evenComponent >>= 1
        maxDivisionsByTwo += 1
    def trial(x):
        if pow(x, evenComponent, candidate) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(x, 2**i * evenComponent, candidate) == candidate - 1:
                return False
        return True
    
    for i in range(numberOfTrials):
        round_tester = random.randrange(2, candidate)
        if trial(round_tester):
            return False
    return True

def multiplicativeInverse(e, phi):
    t, newt = 0, 1
    r, newr = phi, e
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    if r > 1:
        return 'Error: public key is not inverible'
    if t < 0:
        t += phi
    return t

#print(toList('This is a test message.'))
#print(generatePrimeNumber(1024))

if __name__ == "__main__":
    while True:
        print(LOGO)
        answerKeys = input('[o]wn keys or [g]enerate? ').lower()
        if answerKeys not in "go":
            continue
        answerCipher = input('[d]ecode or [e]ncode? ').lower()
        if answerCipher not in "de":
            continue
        if answerKeys == 'o' and answerCipher == 'e':
            small = int(input('Smaller (public) key: '))
            big = int(input('Big key: '))
        elif answerKeys == 'o' and answerCipher == 'd':
            small = int(input('Smaller (private) key: '))
            big = int(input('Big key: '))
        elif answerKeys == 'g':
            bitDepth = int(input('Bit depth: '))
            p = generatePrimeNumber(bitDepth)
            q = generatePrimeNumber(bitDepth)
            n = p*q
            phi = (p - 1) * (q - 1)
            e = 2
            while e<phi:
                if (math.gcd(e, phi) == 1):
                    break
                else:
                    e += 1
            # d = 2
            # while True:
            #     if (d * e) % phi == 1:
            #         break
            #     d += 1
            d = multiplicativeInverse(e, phi)
            print(f"Public key (e): {e}")
            print(f"Private key (d): {d}")
            print(f"Big key (n): {n}")
            big = n
            if answerCipher == 'e':
                small = e
            elif answerCipher == 'd':
                small = d
        
        cipherText = input(f"Enter {'text to encode' if answerCipher == 'e' else 'list to decode'}: ")
        if answerCipher == 'd':
            cipherList = [int(x.strip()) for x in cipherText[1:-1].split(',')]
        else:
            cipherList = toList(cipherText)
        cipherListResult = []
        for num in cipherList:
            cipherListResult.append(int(pow(num, small, big)))
        if answerCipher == 'e':
            print(f'Here is the ciphered list: {cipherListResult}')
        else:
            res = toString(cipherListResult)
            print(f'Here is decrypted text: {res}')