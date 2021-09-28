import os
import sys
import argparse
import itertools as it
import hashlib,binascii


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--nthash', required=False, default=None, action='store', help='NT hash')
	parser.add_argument('-p', '--password', required=False, default=None, action='store', help='Uppercase password')
	parser.add_argument('-np', '--ntpassword', required=False, default=None, action='store', help='File in the format NT:PASSWORD')
	parser.add_argument('-lp', '--lmpassword', required=False, default=None, action='store', help='File in the format LM:PASSWORD')
	parser.add_argument('-nd', '--ntdsdit', required=False, default=None, action='store', help='Ntds.dit file')
	return parser


def get_ntlm(s):
	return binascii.hexlify(hashlib.new('md4', s.encode('utf-16le')).digest()).decode("utf-8")


def get_permutations(passwd):
	return [''.join(x) for x in it.product(*((c.lower(), c.upper()) if c.isalpha() else c for c in passwd))]


def get_passwd(uppercase_passwd, ntlm_hash):
	for p in get_permutations(uppercase_passwd):
		ntlm = get_ntlm(p)
		if ntlm == ntlm_hash:
			return ntlm,p
	return ntlm,""


def calculate_ntds(lmfile, ntdsdit):
	lm_hashes = open(lmfile).read().splitlines()
	ntds_dit =  open(ntdsdit).read().splitlines()
	for l in lm_hashes:
		for n in ntds_dit:
			if l.split(":")[0] in n:
				uppercase_passwd = l.split(":")[1]
				user = n.split(":")[0]
				lmhash = n.split(":")[2]
				nthash = n.split(":")[3]
				ntlm,cleartext_passwd = get_passwd(uppercase_passwd, nthash)
				#print(ntlm+":"+cleartext_passwd)			
				print(user+":"+cleartext_passwd)
				# creds.append(user + ":" + cleartext_passwd)
				### with open("/tmp/test.txt", "a") as myfile:
				### 	myfile.write(user + ":" + cleartext_passwd+"\n")
	


def main():
	args = get_args().parse_args()
	ntlm_hash =         args.nthash
	uppercase_passwd =  args.password
	ntlmfile =          args.ntpassword
	lmfile =            args.lmpassword
	ntdsdit =           args.ntdsdit
	if not (uppercase_passwd is None and ntlm_hash is None):
		ntlm,cleartext_passwd = get_passwd(uppercase_passwd, ntlm_hash)
		print(ntlm+":"+cleartext_passwd)
	elif not (ntlmfile is None):
		if not os.path.isfile(ntlmfile):
			print("[!] File not found")
			sys.exit(0)
		else:
			combs = [(c.split(":")[1],c.split(":")[0]) for c in open(ntlmfile).read().splitlines()]
			for c in combs:
				ntlm,cleartext_passwd = get_passwd(c[0],c[1])
				print(ntlm+":"+cleartext_passwd)
	elif not (lmfile is None and ntdsdit is None):
		if not os.path.isfile(lmfile) or not os.path.isfile(ntdsdit):
			print("[!] File not found")
			sys.exit(0)
		else:
			calculate_ntds(lmfile, ntdsdit)
			
	else:
		get_args().print_help()


if __name__== "__main__":
	main()
