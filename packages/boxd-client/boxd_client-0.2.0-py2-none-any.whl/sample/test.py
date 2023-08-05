# byte[] P = "password".getBytes("UTF-8");
# byte[] S = "NaCl".getBytes("UTF-8");
# int N = 1024;
# int r = 8;
# int p = 16;
# int dkLen = 64;
# String DK = "fdbabe1c9d3472007856e7190d01e9fe7c6ad7cbc8237830e77376634b3731622eaf30d92e22a3886ff109279d9830dac727afb94a83ee6d8360cbdfa2cc0640";


# p = bytes("1", "utf-8")
# s = bytes("NaCl", "utf-8")
# print (p)
# print (p.hex())
n = 262144
r = 1
p = 8
dkLen = 32

from Crypto.Protocol.KDF import scrypt
from Crypto import Random

from eth_utils import (
    big_endian_to_int,
    decode_hex,
    encode_hex,
)

# ret = scrypt("1",  s,  key_len=dkLen, N=n, r=r, p=p, num_keys=1,)
# print (ret.hex())

salt = bytes.fromhex("7ad2f5a0ce8168913e4bb4c969951ca86cd5c1c5169530b722da20cc3cc7f156")
ret = scrypt("1",  salt=salt,  key_len=dkLen, N=n, r=r, p=p, num_keys=1,)
print ([x for x in ret])
print (ret.hex())
print (encode_hex(ret))