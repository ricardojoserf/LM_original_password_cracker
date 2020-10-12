import os
import sys
import argparse
import itertools as it
import hashlib,binascii


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--ntlm_hash', required=False, default=None, action='store', help='NTLM hash')
	parser.add_argument('-p', '--password', required=False, default=None, action='store', help='Uppercase password')
	parser.add_argument('-f', '--file', required=False, default=None, action='store', help='File in the format NTLM:PASSWORD')
	return parser


def get_ntlm(s):
	# source: https://www.trustedsec.com/blog/generate-an-ntlm-hash-in-3-lines-of-python/
	return binascii.hexlify(hashlib.new('md4', s.encode('utf-16le')).digest()).decode("utf-8")


def get_permutations(passwd):
	# source: https://stackoverflow.com/questions/11144389/find-all-upper-lower-and-mixed-case-combinations-of-a-string/11165671
	lu_sequence = ((c.lower(), c.upper()) if c.isalpha() else c for c in passwd)
	return [''.join(x) for x in it.product(*lu_sequence)]


def get_passwd(uppercase_passwd, ntlm_hash):
	for p in get_permutations(uppercase_passwd):
		ntlm = get_ntlm(p)
		if ntlm == ntlm_hash:
			return ntlm,p
	return ntlm,""


def main():
	args = get_args().parse_args()
	uppercase_passwd =  args.password
	ntlm_hash =         args.ntlm_hash
	file =              args.file
	if not (uppercase_passwd is None and ntlm_hash is None):
		ntlm,cleartext_passwd = get_passwd(uppercase_passwd, ntlm_hash)
		print(ntlm+":"+cleartext_passwd)
	elif not (file is None):
		if not os.path.isfile(file):
			print("[!] File not found")
			sys.exit(0)
		else:
			combs = [(c.split(":")[1],c.split(":")[0]) for c in open(file).read().splitlines()]
			for c in combs:
				ntlm,cleartext_passwd = get_passwd(c[0],c[1])
				print(ntlm+":"+cleartext_passwd)
	else:
		get_args().print_help()


if __name__== "__main__":
	main()