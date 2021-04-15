import base64
from random import randrange
from random import randint


def egcd(a,b):
	prevx, x = 1, 0; prevy, y = 0, 1
	while b:
		q = a//b
		x, prevx = prevx - q*x, x
		y, prevy = prevy - q*y, y
		a, b = b, a % b
	return a, prevx, prevy

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def ismillerprime(n, k):
	if n == 1:
		return False
	if n in [2, 3, 5, 7, 11, 13, 17, 19]:
		return True
	for p in [2, 3, 5, 7, 11, 13, 17, 19]:
		if n % p == 0:
			return False
	r = 0
	s = n - 1
	while s % 2 == 0:
		r += 1
		s //= 2
	for i in range(k):
		a = randrange(2, n - 1)
		x = pow(a, s, n)
		if x == 1 or x == n - 1:
			continue
		for j in range(r - 1):
			x = pow(x, 2, n)
			if x == n - 1:
				break
		else:
			return False
	return True


def randomprime(length, millerrounds):
	length -= 1
	start = randint(10 ** length, 10 ** length * 9)
	if start % 2 == 0:
		start += 1
	counter = 0
	isloop = True
	while isloop:
		testnumber = start + (counter * 2)
		if ismillerprime(testnumber, millerrounds):
			isloop = False
		counter += 1
	return testnumber

	
def generatekeys(length, millerrounds):
	p = randomprime(length // 2, millerrounds)
	q = randomprime(length // 2, millerrounds)
	while p == q:
		q = randomprime(length // 2, millerrounds)
	n = p * q
	phin = (p - 1) * (q - 1)
	e = randomprime(length // 2, millerrounds)
	while phin % e == 0 or n % e == 0:
		e = randomprime(length // 2, millerrounds)
	d = modinv(e, phin)
	del p
	del q
	return [[e, n], [d, n]]


def encrypt(number, publickey):
	cipher = pow(number, publickey[0], publickey[1])
	return cipher


def decrypt(cipher, privatekey):
	number = pow(cipher, privatekey[0], privatekey[1])
	return number


def createsignature(message, privatekey):
	signature = pow(message, privatekey[0], privatekey[1])
	return signature


def checksignature(signature, publickey):
	message = pow(signature, publickey[0], publickey[1])
	return message

class BDRSACrypter:

	def __init__(self):
		self.millerRounds = 64
		self.keypair = None

	def GenKeypair(self, bitSize=4096):
		keys =  generatekeys(bitSize, self.millerRounds)
		
		self.keypair = keys

		pubkey = keys[0]
		privkey = keys[1]

		print(keys)		
		pubkeyEncoded = ""
		privkeyEncoded = ""

		for block in pubkey:
			pubkeyEncoded += base64.b64encode((str(block)).encode('ascii')).decode('ascii')+ '\n'

		for block in privkey:
			privkeyEncoded += base64.b64encode((str(block)).encode('ascii')).decode('ascii')+ '\n'

		return [pubkeyEncoded, privkeyEncoded]

	def LoadKeypair(self, keypair):
		pubkey = []
		privkey = []

		pubkeyEncoded = keypair[0]
		privkeyEncoded = keypair[1]

		pubkeyBlocks = pubkeyEncoded.split("\n")
		privkeyBlocks = privkeyEncoded.split("\n")


		for block in pubkeyBlocks:
			blockDecoded = base64.b64decode(block.encode('ascii')).decode('ascii')
			if blockDecoded != '':
				pubkey.append(int(blockDecoded))

		for block in privkeyBlocks:
			blockDecoded = base64.b64decode(block.encode('ascii')).decode('ascii')
			if blockDecoded != '':
				privkey.append(int(blockDecoded))

		print([pubkey, privkey])

		self.keypair = [pubkey, privkey]

	def Encrypt(self, plaintext, pubkey):
		cipher = []
		for i in range(0, len(plaintext)):
			c = encrypt(ord(plaintext[i]), pubkey)
			cipher += [c]
		return cipher

	def Decrypt(self, cipher, privkey):
		plaintext = ""
		for i in range(0, len(cipher)):
			plaintext += chr(decrypt(cipher[i], privkey))
		return plaintext

if __name__ == '__main__':
	crypto = BDRSACrypter()
	kp = crypto.GenKeypair(bitSize=1024)
	print("PUBKEY:\n", kp[0])
	print("PRIVKEY:\n",kp[1])
	crypto.LoadKeypair(kp)

	#ciphertext = crypto.Encrypt("Password1234!", kp[0])

	#plaintext = crypto.Decrypt(ciphertext, kp[1])
	#print(plaintext)