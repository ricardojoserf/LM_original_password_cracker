from passlib.hash import lmhash
import hashlib, binascii
import string
import random
import sys


def get_lm_hash(value):
	return lmhash.hash(value)


def get_nt_hash(value):
	return binascii.hexlify(hashlib.new('md4', value.encode('utf-16le')).digest()).decode("utf-8")


def to_uppercase(value):
	return value.upper()


def create_files(lm_hash, nt_hash, uppercase):
	with open("/tmp/lmpassword.txt", "a") as myfile:
	    myfile.write(lm_hash + ":" + uppercase+"\n")
	with open("/tmp/ntds.dit", "a") as myfile:
	    myfile.write("userx"+":"+"0"+":"+lm_hash+":"+nt_hash+":::"+"\n")


def main():
	for i in range(0,int(sys.argv[1])):
		letters = string.ascii_lowercase
		val = ''.join(random.choice(letters) for i in range(14))
		#val = "password"
		lm_hash = get_lm_hash(val)
		nt_hash = get_nt_hash(val)
		uppercase = to_uppercase(val)
		#print(lm_hash + " " + nt_hash + " " + uppercase)
		create_files(lm_hash, nt_hash, uppercase)


main()
