# Retrieving passwords using NTLM + cracked LM hashes

The first step when creating a LM hash is converting the password to uppercase, so "password" and "pAsSwwOrd" have the same LM hash and the password cracked from these hashes with tools like hashcat is in both cases "PASSWORD", in uppercase (so it is not the correct password). 

However, having the NTLM and a cracked LM hash it is possible to get the original password by testing all the permutations of upper and lowercases. This is useful if a *ntds.dit* file has both NTLM and LM hashes (LM hashes different to *AAD3B435B51404EEAAD3B435B51404EE*).


## Usage

For a single hash

```
python3 main.py -h NTLM_HASH -p UPPERCASE_PASSWORD
```

For a file with a list in the format *NTLM_HASH:UPPERCASE_PASSWORD*:

```
python3 main.py -f ntlm_pass.txt
```

For a file with *LM_HASH:UPPERCASE_PASSWORD* and a ntds.dit file:

```
python3 main.py -l lm_pass.txt -n ntds.dit
```


## Process

Having a ntds.dit file *ntds.dit*, first crack the LM hashes:

```
hashcat -m 3000 -a 3 ntds.dit ?a?a?a?a?a?a?a
```

Dump the results (the file has the format *LM_Hash:UPPERCASE_PASSWORD*):

```
hashcat -m 3000 ntds.dit --show | sort -u | tee lm_pass.txt
```

Retrieve the cleartext passwords with the script:

```
python3 main.py -l lm_pass.txt -n ntds.dit
```


Get a list with the format *NTLM_HASH:UPPERCASE_PASSWORD*:

```
for i in $(cat lm_pass.txt); do lm=$(echo $i | cut -d ":" -f 1); pass=$(echo $i | cut -d ":" -f 2); ntlm=$(cat ntds.dit | grep $lm | cut -d ":" -f 4 | sort -u) ; for n in $ntlm; do echo $n":"$pass; done; done | tee ntlm_pass.txt
```

Retrieve the cleartext passwords with the script:

```
python3 main.py -f ntlm_pass.txt
```
