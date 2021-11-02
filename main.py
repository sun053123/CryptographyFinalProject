import random


# TODO initail state ต้องกด Generate Key เก็บค่าก่อนเท่านั้น ต้องกดตัวเลือก 1 2 หรือ 3 ก่อน
class PrivateKey(object):  # เก็บค่า Private keys ทั้งหมด และเก็บ pubkey ที่เป็น ขนาดของบิท p และ g ด้วย
    def __init__(self, p=None, g=None, x=None, bitLenght=0):
        self.p = p
        self.g = g
        self.x = x
        self.bitLenght = bitLenght


class PublicKey(object):  # เก็บค่า Public keys และ ขนาดของบิท p
    def __init__(self, p=None, g=None, h=None, bitLenght=0):
        self.p = p
        self.g = g
        self.h = h
        self.bitLenght = bitLenght


class DataEncDec(object):  # เก็บ ciphertext , plaintext เป็น bytearray
    def __init__(self, cipher=None, plain=None):
        self.cipher = cipher
        self.plain = plain


class SignatureElgamal(object):  # เก็บค่า r , s ของ Elgamal Signature
    def __init__(self, signedtxt=None, verifytxt=None, r=None, s=None):
        self.signedtxt = signedtxt
        self.verifytxt = verifytxt
        self.r = r
        self.s = s


def gcd(a, b):  # ใช้ หรม ด้วย Euclid Algolithm # https://www.geeksforgeeks.org/gcd-in-python/
    while a != 0:  # a จะเทียบ b และนำ a ใน while นั้นเก็บค่าไว้ก่อน (a ตัวแรกใน loop )จากนั้นจะทำการ b = b mod a และทำจนกว่า a จะได้ 0 จะส่งb รอบสุดท้ายกลับไป
        a, b = b % a, a
        # print("b in gcd = ",b)
        # print("a in gcd = ", a)
    return b  # ส่งไปแต่ละค่าและจะเช็ค หรม #ในตอนที่ทดค่า b คือถ้าได้ค่าออกไปเป็น 1 แล้วคือตอนสุดท้ายที่ทำ while จะได้ค่าที่ถูกต้องของ rand no.


def power(a, b):
    sum = 1
    while b >= 0:
        sum = sum * a
        b -= 1
        # print(b , sum)#ค่า sum จะถูกคูณด้วย a และเพิ่มขึ้นมาก ๆ ไปเรื่อย ๆ จนกว่า b = 0 (จาก 128)
    return sum  # ทำตั้งแต่ b = 128 ไล่มาเรื่อย ๆ จนเจนหมดใช้ค่า sum * a จะได้ผลในloopเพิ่มขึ้นเมื่อทำถึง -1
    # return ค่า sum กลับไปเช็ค findprime while(1): และ randomใหม่ถ้ายังไม่ใช่ค่าที่ถูก(กลับมาทำตรงนี้ใหม่เมื่อ return power ไปไม่ใช่ค่า primeที่เช็คใน isprime)


# https://www.programiz.com/python-programming/examples/prime-number
# TODO lehmann test p = bitlenght ,t = confidence or try round
# ค่าที่รับมาตรงนี้ p = ที่เรา rand มาแล้ว check แล้ว t = 100
def isPrime(p, t):
    a = random.randint(2, p - 1)  # alpha
    expo = (p - 1) // 2  # alpha pow จากสูตรที่มันกำลัง n-1 // 2

    if p % 2 == 0:  # เพราะ p ไม่ใช่เลขคู่
        return False

    while t > 0:  # ทำตามรอบ try
        result = modexp(a, expo, p)  # rand หา a เลื่อย ๆ try รอบตาม confidence เพื่อมาเช็ค result ให้ == 1 หรือ == -1
        if result == 1 or result == p - 1:  # เพราะ alpha จะต้องไม่เท่ากับอันนี้
            a = random.randint(2, p - 1)
            t -= 1
            # print(t , a)
        else:
            return False  # Not Prime มันก็จะไม่หลุด loop gen p มาใหม่ใน find prime
    return True  # Prime ได้ ture แล้วได้ return ในการ check isprime เลย


def FindInverse(n2, n1):  # Iterateive Version is faster and uses much less stack space
    tempMod = n1
    r, q = (n1 % n2, n1 // n2)
    a1, b1, a2, b2 = (1, 0, 0, 1)  # initial state ทุกครั้ง
    while r != 0:
        tempA2 = a2
        tempB2 = b2
        a2 = a1 - q * a2
        b2 = b1 - q * b2
        a1, b1 = tempA2, tempB2
        n1, n2 = n2, r
        r, q = (n1 % n2, n1 // n2)
    if n2 != 1:
        return -1  # GCD ไม่เท่ากับ 1
    return b2 % tempMod


def modexp(base, exp, modulus): return pow(base, exp, modulus) \
    # , print("g = " + str(pow(base, exp, modulus)) + " - org - "+ str(base) + ","+ str(exp) + "," + str(modulus))


def GenRandom(p):  # ค่า k คือ random no และมีกฎดังนี้ k โดยที่ทำ gcd (k , p-1) = 1 ถึงจะสามารถนำมาใช้ได้
    key = random.randrange(1, p - 1)
    while gcd(key, p - 1) != 1:  # ตามสูตรเช็คค่า gcd จะต้องได้เท่ากับ 1 ถ้าไม่เป็นจะ random เช็คใหม่ใน loop ใน gcd
        key = random.randrange(1, p - 1)
    return key  # ค่า K random number นั่นเอง สรุปแล้วถ้าทำ gcd ให้ออกมาเท่ากับ 1 ถ้าไม่ได้จะสุ่มใหม่ หาจนกว่าจะเจอนั่นเอง


def find_prime(bitLenght,
               confidence):  # ค่า bitlenght คือค่าที่เราจะนำมาใช้กำหนดขนาด bit ของp และ confidence คือค่าที่เรานำมาทำ lehmann
    while (1):  # loopwhile ทำจนกว่าจะเป็นจริงได้ค่า True while loop
        p = random.randint(2 ** (bitLenght - 2), 2 ** (bitLenght - 1))  # init rand prime for make parameter
        # print("p first ",p)
        if p >= power(2, bitLenght - 2) or p <= power(2,
                                                      bitLenght - 1):  # ใส่ 2 เพื่อค่าจะได้โต sum ไม่สามารถเป็น 1 ใน power
            # มันคือค่าจำนวนของ bit ที่ควรจะสุ่มได้ใน range bitlenght นั้นๆ 2**128-1 และ range ของ 2**128
            # มันเข้ามาเช็คว่า p>= ตัวแรกมันคือค่าจำนวนที่การสุ่มที่ว่าด้วย 126 - 128 บิทเนี่ยจะต้องมากกว่า 128 - 2 = 126 ตัว และไม่มสกกว่า 128 - 1 = 127
            while True:
                if isPrime(p, confidence):
                    # p is 126-127 bit จะหาcheck isPRimeloop ว่าเป็น prime ไหมถ้าไม่ก็ไป  แล้วทำต่อ
                    # chech safe prime
                    return p  # ถ้าเช็คแล้วเป็นจริงส่ง p ได้เลย
                p += 1  # check ในรูปเรื่อย ๆ และเมื่อไม่ใช่ isPrime ใน ค่า confidence รอบ มันจะ +1 ตัวเองแล้วเข้า check is prime ใหม่
                # เมื่อ Check แล้วเป็น flase กลับมาจะไม่หลุด loop while และจำให้ this:P +1 เพื่อเข้าไป check isPrime หลายรอบ
        else:
            -1, print("bruh Fail")

    # print("Fail") #loop while ไม่มีทางทำค่านี้


def find_prime_file(keySize, file):
    # TODO อ่านไฟล์ที่ถูกเขียนด้วย ASCII ฐาน 16HEX -> ByteString ด้วยการอ่านเป็น Byte -> แต่เราใช้ DECฐาน10ไป
    #  เมื่อเราทำ ค่าเป็น dec (ไม่prime) แล้วจะได้ lenght 128 max และไม่ต้องสุ่มจะเข้าหา  prime เลย หาจนได้และส่งกลับ
    # 0 -> f ทั้งหมด 16 ตัว # hex = ff byte 0000 0000 = 2byte
    f = open(file, "rb")
    byte = f.read()
    readByte = keySize // 8
    # ทำการหาร 8 เพราะ 0011 0001 มี 8 ตัว เอามาเป็น lenght ของการ readbyte
    # จำกัด block ความยาว bitlenght

    delete00 = 0
    while byte[delete00] == 0:
        delete00 += 1
    i = delete00

    bitString = ''.join(format(i, '08b') for i in byte[delete00:(delete00 + readByte + 2)])
    bitStringforprintONLY = ', '.join(format(i, '08b') for i in byte[delete00:(delete00 + readByte + 2)])
    print('bitSforptint only ', bitStringforprintONLY)  # แสดงแบบตัดคำ
    # จะเห็นว่า 00110001,00110101,01000010 จะมี 00 ต่อหน้าเสมอเพราะ Hex -> bin
    # จะเผื่อไว้ข้างหน้า 00x แต่เราไม่ได้ใช้ range นี้ จะต้องตัดมันออก โดยการเอา i ที่ได้จาก delete00

    findOne = 0  # ทำการหา 1 ทุกๆ i ว่าเรื่มตั้งแต่ตัวที่เท่าไร เช่น 00110001
    for i in range(0, len(bitString)):
        if bitString[i] == '1':
            findOne = i + 1
            break
    # print("findOne  = " , findOne)

    bitString = bitString[(findOne - 1):keySize + (findOne - 1)]
    print('bitS + findOne = decNotprime =', bitString)  # printแบบตัด0แล้ว
    decNotprime = int(bitString, 2)
    # แปลง bitString ที่ตัด 0 ข้างหน้าออกไปแล้วเพื่อทำการแปลงความยาวทั้งหมด
    # เช่น 1101101100...127ตัว = 38ตัวของ DEC เป็น dec ที่ไม่ prime
    print('decimal in this line is not a prime number', decNotprime)
    # ได้ dec ผสม lenght แล้วแต่ต้องไปทำให้เป็น prime

    # เข้า loop เหมือนตอนหา prime แต่อันที่แล้วเป็นแบบสุ่มค่า อันนี้เรา get ค่าเข้า if เลย
    # if decimal >= 2**(n-1) or decimal <= 2**n:
    if decNotprime >= power(2, keySize - 1) or decNotprime <= power(2, keySize):
        while True:
            if isPrime(decNotprime, keySize):
                return decNotprime
            decNotprime += 1
            # เมื่อ Check แล้วเป็น flase กลับมาจะไม่หลุด loop while และจำให้ this:P +1 เพื่อเข้าไป check isPrime หลายรอบ
    else:
        -1, print("bruhFail")


def find_primitive_root(p):
    if (p == 2):
        return -1
    # ถ้า p - 1 จะหาร 2 ลงตัว in practicular if p=2p+1 where p1 is also prime
    # loop นี้จะ random หา g จนกว่าจะเจอ primitive root mod P
    while (1):
        g = random.randint(2, p - 1)  # gen alpha
        # print("grand",g) #gen ไม่กี่รอบ
        # g is a primitive root if for all prime factors of p-1, p[i]
        # g^((p-1)/p[i]) (mod p) is ไม่สอดคล้อง to 1
        # check คุณสมบัติของ g คือ
        # alpha in Zp* และ alpha ไม่เท่ากับ 1 mod p  # check alpha pow p-1/2 จะไม่เท่ากับ 1 mod p
        if (isPrime(p, 100) == True):  # g pow p2 mod p == 1 mod p
            if (isPrime((p - 1) // 2, 100) == False):
                if modexp(g, (p - 1) // 2, p) != 1 or modexp(g, (p - 1) // 2, p) != (p - 1):
                    print("gg ", g)
                    return g

    # สามารถทำ Function FastExpo ได้เองดังนี้
    # TODO -- Fast Exponential -- #
    #  รับค่า 3 ตัว Base Expo Mod โดยยังไม่ต้องดักค่าเพราะจะไปทำข้างในนี้
    #  base = g
    #  expo = (p-1 // p1)    {หมายเหตุ // <-- หารปัดเศษทิ้งจะไม่มีทศนิยม 15 / 2 = 14}
    #  mod = p ซึ่งแน่นอนว่าต้อง Mod P !

    # setcheck = 1 เพื่อสร้างค่าเทียบ
    # if 1 & expo: #เข้า loop if นี้เพื่อเช็ค expo ค่าที่ส่งมาคือ 1 หรือจาก การเช็ค expo = (p-1 // p1) ใน func findPrimativeroot
    #     setcheck = base # เพื่อให้ g = 1
    # while expo:
    #     expo = expo >> 1
    #     base = (base * base) % mod    # บรรทัดนี้
    #     if expo & 1:
    #         setcheck = (base * sum) % mod
    # return setcheck


def generate_keys(bitLenght=int(128), confidence=int(100)):
    # todo กดหนดค่า ความยาวและระยะต่ำสุดไว้ 128-80 ของP ที่เป็น safeprime และ G  ที่เป็น Gpow2 mod p เพื่อยากระดับความปลอดภัย sk จะมีค่าใน setprimt จึง //2 ได้
    # p is the prime
    # g is the primitve root
    # x is random in (0, p-1 //2 ) inclusive
    # h = g ^ x mod p

    p = find_prime(bitLenght, confidence)
    # print("p is in keygenerator= " + str(p))
    # p finale แล้ว p ที่ check ว่า Prime แล้วมา print ตรงนี้ 127 bit #39 ตัวของ dec
    g = find_primitive_root(p)
    # print("g 1st is = " + str(g)) #g finale แล้ว จะมี 126 bit #38 ตัวของ dec
    g = modexp(g, 2,
               p)  # g pow 2 mod p เพื่่อ increase security เพิ่มขึ้น ดังนี้ g = h pow 2 mod p โดยที่ h เป็นซับเซ้ท Zp*
    # print("g2 = " ,g) # ได้ค่า g จริง ๆ
    # print("g 2nd is = " + str(g))  # g finale แล้ว จะมี 126 bit #38 ตัวของ dec
    x = random.randint(1, (p - 1) // 2)  # สุ่มค่าตัวใน P จึงสามารถมี //2
    # print("x " + str(x))
    h = modexp(g, x, p)
    # print("h " + str(h))
    # print("x " + str(x))
    publicKey = PublicKey(p, g, h, bitLenght)
    privateKey = PrivateKey(p, g, x, bitLenght)

    return {'privateKey': privateKey, 'publicKey': publicKey, 'p': p, 'g': g, 'x': x, 'h': h}


# p = 329581202407119856424693276880252591947 #128b
# g = 130067083687254989583436867900911453882 #127b
# x = 1456662116680671893048483588325800054 #121b
# h = 60004853357862471643567287385757677797 #126b


def generate_keys_file(keySize, file):
    bitLenght = keySize
    p = find_prime_file(keySize, file)
    # print("p is infilegenkey = " + str(p))
    # p finale แล้ว p ที่ check ว่า Prime แล้วมา print ตรงนี้ 127 bit #39 ตัวของ dec

    g = find_primitive_root(p)
    # print("g 1st is = " + str(g)) #g finale แล้ว จะมี 126 bit #38 ตัวของ dec
    # TODO เมื่อ Textfile ไม่เปลี่ยน p ไม่เปลี่ยน และ g เปลี่ยนเพราะเกิดจากการ gen

    g = modexp(g, 2, p)
    # print("g 2nd infilegenkey is = " + str(g))
    # g finale แล้ว จะมี 126 bit #38 ตัวของ dec

    x = random.randint(1, (p - 1) // 2)
    # print("x " + str(x))

    h = modexp(g, x, p)
    # print("h infilegenkey " + str(h))
    # print("x infilegenkey " + str(x))

    publicKey = PublicKey(p, g, h, bitLenght)
    privateKey = PrivateKey(p, g, x, bitLenght)

    return {'privateKey': privateKey, 'publicKey': publicKey, 'p': p, 'g': g, 'x': x, 'h': h}


def bypasskey(p, g, h, bitLenght):
    publicKey = PublicKey(p, g, h, bitLenght)
    privateKey = PrivateKey(p, g, bitLenght)

    return {'privateKey': privateKey, 'publicKey': publicKey, 'p': p, 'g': g, 'h': h}


def bypasskey2(r, s):
    signatureElgamal = SignatureElgamal(r, s)
    return {'signatureElgamal': signatureElgamal, 'r': r, 's': s}


def encode(sPlaintext, iNumBits):
    byte_array = bytearray(sPlaintext, 'utf-8')

    # y o u
    # a -> ascii no
    # a -> 00110100

    # z is the array of integers mod p
    z = []
    # each encoded integer will be a linear combination of k message bytes
    # k must be the number of bits in the prime divided by 8 because each
    # message byte is 8 bits long
    k = iNumBits // 8

    # utf8 =  0000 0000 ,มาจาก ascii
    # j marks the jth encoded integer (J FLAG)
    # j will start at 0 but make it -k because j will be incremented during first iteration
    j = -1 * k
    # num is the summation of the message bytes
    num = 0
    # i iterates through byte array
    for i in range(len(byte_array)):
        # if i is divisible by k, start a new encoded integer
        if i % k == 0:
            j += k
            num = 0
            z.append(0)
        # add the byte multiplied by 2 raised to a multiple of 8
        z[j // k] += byte_array[i] * (2 ** (8 * (i % k)))

    # example
    # if n = 24, k = n / 8 = 3
    # z[0] = (summation from i = 0 to i = k)m[i]*(2^(8*i))
    # where m[i] is the ith message byte

    # return array of encoded integers
    return z
    # decodes integers to the original message bytes


def decode(aiPlaintext, iNumBits):
    # bytes array will hold the decoded original message bytes
    bytes_array = []

    # same deal as in the encode function.
    # each encoded integer is a linear combination of k message bytes
    # k must be the number of bits in the prime divided by 8 because each
    # message byte is 8 bits long
    k = iNumBits // 8

    # num is an integer in list aiPlaintext
    for num in aiPlaintext:
        # get the k message bytes from the integer, i counts from 0 to k-1
        for i in range(k):
            # temporary integer
            temp = num
            # j goes from i+1 to k-1
            for j in range(i + 1, k):
                # get remainder from dividing integer by 2^(8*j)
                temp = temp % (2 ** (8 * j))
            # message byte representing a letter is equal to temp divided by 2^(8*i)
            letter = temp // (2 ** (8 * i))
            # add the message byte letter to the byte array
            bytes_array.append(letter)
            # subtract the letter multiplied by the power of two from num so
            # so the next message byte can be found
            num = num - (letter * (2 ** (8 * i)))

    # example
    # if "You" were encoded.
    # Letter        #ASCII
    # Y              89
    # o              111
    # u              117
    # if the encoded integer is 7696217 and k = 3
    # m[0] = 7696217 % 256 % 65536 / (2^(8*0)) = 89 = 'Y'
    # 7696217 - (89 * (2^(8*0))) = 7696128
    # m[1] = 7696128 % 65536 / (2^(8*1)) = 111 = 'o'
    # 7696128 - (111 * (2^(8*1))) = 7667712
    # m[2] = 7667712 / (2^(8*2)) = 117 = 'u'
    decodedText = bytearray(b for b in bytes_array).decode('utf-8')

    return decodedText

    # encode -> encrypt -> decrypt (encode ในรูปแบบของ mod ascii ยังอ่านไม่ได้) ->  decode -> ได้ ptext.decode utf8
    # org ctext (a b)
    # ptext = encode ( 313131313 i=1 , 1312313 i=2 , 113123 ,1313231313 ......)
    #
    # ctext = ((a0=i1 b0=i1)   ,  a1=i2 b1=i2 ....)
    # dec (a0b0 -> p0=i1 , a1b1 = i2 .....)
    # i = block นึงของการ encode


def encrypt(ptext, pub):
    # org ctext = (a,b)
    # this ctext = [(a[0] ,b[0] , a[1] ,b[1] . . . . .
    # message = ''.join(format(ord(x)) for x in ptext)
    # print("plaintxt ascii = ", message)

    z = encode(ptext, pub.bitLenght)
    print("encoded(block) text = ", z)

    # cipher_pairs list will hold pairs (c, d) corresponding to each integer in z
    cipher_pairs = []
    pop = 0
    # i is an integer in z

    for i in z:
        k = GenRandom(pub.p)  # random number
        # y = random.randint(0, pub.p)
        # c = g^y mod p
        c = modexp(pub.g, k, pub.p)
        # d = ih^y mod p
        d = (i * modexp(pub.h, k, pub.p)) % pub.p
        # add the pair to the cipher pairs list
        # print(d)
        cipher_pairs.append([c,
                             d])  # ทำการ pair append กันทีละคู่ค่าจะเพิ่มทีละ 2 คู่เพราะเริ่มจาก0 - 2 - 4 - 6 = c และ คี่ = d 1 - 3 - 5 - 7
        pop += 1
        # print(cipher_pairs , pop) #ทำ *2 ของ index z ดังนั้น z คือ plaintext cipher จึงได้ 2เท่านั่นเอง
    encryptedStr = ""
    for pair in cipher_pairs:
        encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '

    cipher = encryptedStr
    dataEncDec = DataEncDec(cipher)
    return {'dataEncDec': dataEncDec, 'cipher': cipher}


def decrypt(priv, cipher):
    # decrpyts each pair and adds the decrypted integer to list of plaintext integers
    plaintext = []
    pop = 0
    cipherArray = cipher.split()
    # if (not len(cipherArray) % 2 == 0):
    # return "Malformed Cipher Text"
    for i in range(0, len(cipherArray), 2):
        # c = first number in pair
        c = int(cipherArray[i])
        # d = second number in pair
        d = int(cipherArray[i + 1])

        # s = c^x mod p
        s = modexp(c, priv.x, priv.p)
        # plaintext integer = ds^-1 mod p
        plain = (d * modexp(s, priv.p - 2, priv.p)) % priv.p  # p - 1 จะได้ตัวมันเอง ต้อง (P - 1) - 1
        # add plain to list of plaintext integers
        plaintext.append(plain)
        pop += 1
        print(plaintext, pop)

    print("ptextc = ", plaintext)
    decryptedText = decode(plaintext, priv.bitLenght)

    return str(decryptedText)


def encryptFile(filetext, pub):
    f = open(f'{filetext}', 'rb')
    ptextb = f.read().decode('utf-8')

    print(ptextb)
    ptext = str(f.read())
    z = encode(ptextb, pub.bitLenght)
    print("encoded(block) text = ", z)

    bitString = ''.join(format(i) for i in ptextb)
    print("text byte= ", bitString)

    # signedtxt = [int(bitString[i:i + 8], 2) for i in range(0, len(bitString), 8)]
    # print("ascii no ptext", signedtxt)

    # s = ''.join(chr(i) for i in signedtxt)
    # print(s) #พริ้นออกมาเป็น ascii no -> word char

    # cipher_pairs list will hold pairs (c, d) corresponding to each integer in z

    cipher_pairs = []
    pop = 0
    # i is an integer in z
    k = GenRandom(pub.p)
    for i in z:
        # y = random.randint(0, pub.p)
        # c = g^y mod p
        c = modexp(pub.g, k, pub.p)
        # d = ih^y mod p
        d = (i * modexp(pub.h, k, pub.p)) % pub.p
        # add the pair to the cipher pairs list
        # print(d)
        cipher_pairs.append([c,
                             d])  # ทำการ pair append กันทีละคู่ค่าจะเพิ่มทีละ 2 คู่เพราะเริ่มจาก0 - 2 - 4 - 6 = c และ คี่ = d 1 - 3 - 5 - 7
        pop += 1
        # print(cipher_pairs , pop) #ทำ *2 ของ index z ดังนั้น z คือ plaintext cipher จึงได้ 2เท่านั่นเอง

    # print(cipher_pairs)

    encryptedStr = ""
    for pair in cipher_pairs:
        encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '

    cipher = encryptedStr
    dataEncDec = DataEncDec(cipher)

    f = open(f'ciphertext.txt', 'w')
    f.write(encryptedStr)  #
    f.close()

    return {'dataEncDec': dataEncDec, 'cipher': cipher}


def decryptFile(priv, cipher):
    f = open(f'{cipher}', 'rb')
    cipher = f.read()

    print("ct = ", cipher)

    # decrpyts each pair and adds the decrypted integer to list of plaintext integers
    plaintext = []

    cipherArray = cipher.split()
    # if (not len(cipherArray) % 2 == 0):
    # return "Malformed Cipher Text"
    for i in range(0, len(cipherArray), 2):
        # c = first number in pair
        c = int(cipherArray[i])
        # d = second number in pair
        d = int(cipherArray[i + 1])
        # s = c^x mod p
        s = modexp(c, priv.x, priv.p)
        # plaintext integer = ds^-1 mod p
        plain = (d * modexp(s, priv.p - 2, priv.p)) % priv.p
        # add plain to list of plaintext integers
        plaintext.append(plain)

    print("ptextc = ", plaintext)
    decryptedText = decode(plaintext, priv.bitLenght)

    return decryptedText


def Hash(k, pub, M):
    p = pub.bitLenght
    pkp = pub.p

    message = ''.join(
        format(ord(x), '08b') for x in M)  # function ORD คืออ่านแปลงตัวอักษรเป็นตัวเลข ของ ASCII = ascii byte
    alpha = len(message)  # IV ขนาดความยาวของ message
    blockString = []
    index = 0
    while len(message) > 0:
        blockString.append(message[:p])
        message = message[p:]
        if len(blockString[index]) != p:
            while len(blockString[index]) != p:
                blockString[index] += blockString[index][-1]
        index += 1

    # TODO Hash
    #  Hash เเต่ละ block เกิดมาจากค่า hash ของ block ที่เเล้วมาบวกกับผลรวมของค่า hash ของ block ย่อยใน block ปัจจุบัน
    #  หาก block นั้นเป็น block เเรกให้ใช้ length เป็นค่า hash ของ block ก่อนหน้า (IV)

    pop = 0
    isFirstRound = True
    hashBlock = []
    lenght = 0

    while len(blockString) > 0:  # ตาม block ที่หามาข้างบนความยาว index
        block = blockString[:k - 1]
        # print("b1 - " ,block) #block ความยาว = 1

        # Padding blockสุดท้ายให้เต็มก่อน hash
        if len(block) != k - 1:
            while len(block) != k - 1:
                block.append(block[-1])

        # print("full block padding = ",block) #block ความยาว = ptext ที่เราใส่ เพราะเราจะทำทั้งหมดและแปลงเป็นเลข Byte
        binaryBlock = ''.join(block)  # รวม block เป็น str ตัวเดียวเพื่อคำนวณ
        if isFirstRound:  # ทำ hash ตัวที่  h1 รับค่า alpha เป็น IV ตัวแรกที่กำหนดคือ ขนาดของ Message
            binaryBlock = format(alpha, 'b') + binaryBlock
            iHashValue = int(binaryBlock, 2) % pkp  # ค่า sum ของ H แต่ละรอบ (อันนี้ H1 only)
            hashBlock.append(iHashValue)
            isFirstRound = False  # flase รอบแรกจะไปทำ else ต่อ
            print("sub -1 ", iHashValue)
        else:  # block  รอบที่เหลือเข้า else
            binaryBlock = format(hashBlock[lenght - 1], 'b') + binaryBlock
            iHashValue = int(binaryBlock, 2) % pkp  # ค่า sum ของ H แต่ละรอบ
            hashBlock.append(iHashValue)
            pop += 1
            print("sub ", iHashValue, pop)

        # print("hashblock = ",hashBlock)
        blockString = blockString[k - 1:]
        lenght += 1

    print("sum of all iHashvalue list of Hash = ", sum(hashBlock[:-1]), " + power(f)", power(hashBlock[-1], 2),
          " % Lenght ", pkp)
    hashValue = (sum(hashBlock[:-1]) + power(hashBlock[-1], 2)) % pkp
    print("sum = ", hashValue)

    f = open(f'hashbin.txt', 'w')
    f.write(str(block))
    f.close()
    print("hashvalue = ", hashValue)
    return hashValue


def hashFile(k, bitLenght, filetext):
    f = open(f'{filetext}', 'rb')
    byteSignMessage = f.read()

    bitString = ''.join(format(i, '08b') for i in byteSignMessage)
    print("bf hash sign = ", bitString)

    hash = Hash(k, bitLenght, bitString)

    return hash


def signMessage(filetext, priv, pub):
    p = pub.p
    g = pub.g
    x = priv.x
    b = []
    k = 7
    bitlenght = pub.bitLenght

    # print(bitlenght)

    f = open(f'{filetext}', 'rb')
    byteSignMessage = f.read()

    bitString = ''.join(format(i, '08b') for i in byteSignMessage)
    print("bf hash sign = ", bitString)

    hashMessage = Hash(k, pub, bitString)  # ได้ value
    print(hashMessage)

    K = GenRandom(pub.p)
    r = modexp(g, K, p)  # เหมือน H
    kInverse = FindInverse(K, p - 1)
    s = (kInverse * (hashMessage - (x * r))) % (p - 1)

    signedtxt = [int(bitString[i:i + 8], 2) for i in
                 range(0, len(bitString), 8)]  # เราจะหากลับจาก byte 00000000 8ตัว ไปเป็น acii number
    print("signedtxt dec ", signedtxt)

    # print("r = ", r) #print text r s
    # print("s = ", s)

    tr = str(r)
    ts = str(s)

    f = open(f'{filetext}', 'rb')
    byteSignMessage = f.read().decode('utf-8')
    f = open(f'msigned.txt', 'w')
    f.write(str(byteSignMessage))
    f.write(str(","))
    f.write(tr)
    f.write(str(","))
    f.write(ts)
    f.close()

    signedtxt = format(', '.join(hex(x)[0:] for x in signedtxt))  # เก็บเข้่า class มี 0x  เป็นฐาน 16

    signatureElgamal = SignatureElgamal(r, s, signedtxt)
    return {'signatureElgamal': signatureElgamal, 'r': r, 's': s, 'signedtxt': signedtxt}


def verifyMessage(verifile, pub):
    p = pub.p
    g = pub.g
    h = pub.h
    bitLenght = pub.bitLenght
    k = 7

    f = open(f'{verifile}', 'rb')
    signMessage = f.read().decode().split(",")

    # s = int(s)
    # r = int(r)

    r = int(signMessage[-2], 10)
    s = int(signMessage[-1], 10)

    print("r = ", r)
    print("s = ", s)
    print("signMessage = ", signMessage[:1])

    bitString = ''.join(format(i) for i in signMessage[:1])
    print(bitString)

    signBinaryMessage = ''.join(format(ord(i), '08b') for i in bitString)
    print(signBinaryMessage)

    X = Hash(k, pub, signBinaryMessage)
    print("X = ", X)

    gx = modexp(g, X, p)
    print("gx = ", gx)

    hr = modexp(h, r, p)
    print("hr = ", hr)
    rs = modexp(r, s, p)

    print("rs = ", rs)
    print("verify value = ", (hr * rs) % p)

    if gx == (hr * rs) % p:
        return True
    return False


def main():
    while True:

        choice = int(input(
            "1. Press '1' to generate keys with Random P.\n"
            "2. Press '2' to generate keys with read file.\n"
            "3. Press '3' to get keys.\n"
            "4. Press '4' to encrypt text.\n"
            "5. Press '5' to decrypt text.\n"
            "6. Press '6' to encrypt file.\n"
            "7. Press '7' to decrypt file.\n"
            "8. Press '8' to get signature keys.\n"
            "9. Press '9' to sign message file.\n"
            "10. Press '10' to verify message file.\n"
            "11. Press '11' to hash.\n"
            "Exit. Press '0' to Exit.\n"
            "your input = "))
        print("\n--------------------------------------------------"
              "--------------------------------------------------"
              "--------------------------------------------------")

        if choice == 1:
            keys = generate_keys()
            priv = keys['privateKey']
            pub = keys['publicKey']

            print(" Generate Keys Sucessful ... ")
            print("p = ", keys['p'])
            print("g = ", keys['g'])
            print("h = ", keys['h'])
            print("x = ", keys['x'])

            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 2:
            print(
                "≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Generate Key with read file ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            keySize = 128
            keyFile = "keystatic.txt"
            keys = generate_keys_file(keySize, keyFile)
            priv = keys['privateKey']
            pub = keys['publicKey']

            print(" Generate Keys Sucessful ... ")
            print("p = ", keys['p'])
            print("g = ", keys['g'])
            print("h = ", keys['h'])
            print("x = ", keys['x'])
            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 3:
            print(
                " ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ GetKey ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            p = input(str("ค่า P = "))
            g = input(str("ค่า G = "))
            h = input(str("ค่า H = "))

            p = int(p)
            g = int(g)
            h = int(h)
            bitLenght = 128

            keys = bypasskey(p, g, h, bitLenght)
            priv = keys['privateKey']
            pub = keys['publicKey']
            print(" Keys saved successful ... ")
            print("p = ", keys['p'])
            print("g = ", keys['g'])
            print("h = ", keys['h'])
            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 4:
            print(
                " ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Encrypt input text ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            ptext = input(str("คำที่จะเข้ารหัส = "))
            enc = encrypt(ptext, pub)

            print('enc = ', enc)
            cipher = enc['cipher']
            print("cipher = ", cipher)
            print("\n Encrypt successful ... ")
            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 5:
            print(
                " ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Decrypt input text ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            dec = decrypt(priv, cipher)
            print(str(dec))
            print("\n Decrypt successful ... ")
            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 6:
            print(
                " ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Encrypt input file ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            filetext = input(str("ไฟล์ที่จะเข้ารหัส = "))
            encryptFile(filetext, pub)
            print("\n Encrypt successful ... ")
            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 7:
            print(
                " ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Decrypt input file ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            filetext = input(str("ไฟล์ที่จะถอดรหัส = "))
            dec = decryptFile(priv, filetext)
            print(dec)
            print("\n Decrypt successful ... ")
            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 8:
            print(
                " ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Get Sign Key ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            # r = input(str("ค่า r = "))
            # s = input(str("ค่า s = "))
            #
            # r = int(r)
            # s = int(s)
            #
            # sign = bypasskey2(r, s)
            # sigkey = sign['signatureElgamal']

            # print(" Keys saved successful ... ")
            # print("r = ", sign['r'])
            # print("s = ", sign['s'])

            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")


        elif choice == 9:
            print(" ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Sign Message ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            filetext = input(str("ชื่อไฟล์ที่เป็น Text จะนำมา = "))
            sign = signMessage(filetext, priv, pub)
            print(" ----- signtxt sucessful -----")
            print("SingedText = ", sign['signedtxt'])
            print("r = ", sign['r'])
            print("s = ", sign['s'])

            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 10:
            print(" ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Verify Message ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            # s = sign['s']
            # r = sign['r']
            # print("rm ", r)
            # print("sm ", s)
            verifile = input(str("ชื่อไฟล์ที่เป็น Text จะนำมา = "))
            veri = verifyMessage(verifile, pub)
            print("this text is ", veri)

            print(" ----- verify finished -----")
            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 11:
            print(" ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈ Hash ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈\n")
            message = input(str("ชื่อไฟล์ที่เป็น Text จะนำมา = "))
            k = 7
            hashFile(k, pub.bitLenght, message)

            print(" ----- hash sucessful -----")
            print("\n--------------------------------------------------"
                  "--------------------------------------------------"
                  "--------------------------------------------------\n")

        elif choice == 0:
            exit()


if __name__ == "__main__":
    main()
