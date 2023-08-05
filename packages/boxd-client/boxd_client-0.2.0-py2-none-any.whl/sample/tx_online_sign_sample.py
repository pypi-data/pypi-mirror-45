#!/usr/bin/env python3

import time

from boxd_client.boxd_client import BoxdClient

from eth_utils import (
    big_endian_to_int,
    decode_hex,
    encode_hex,
)

boxd = BoxdClient("39.97.169.1", 19111)


priv_key_hex = "5ace780e4a6e17889a6b8697be6ba902936c148662cce65e6a3153431a1a77c1"
addr = "b1USvtdkLrXXtzTfz8R5tpicJYobDbwuqeT"
amount = 10000
fee = 100

to = {}
to["b1Tvej4G8Lma86pgYpWqv4fUFJcEyDdeGst"] = 100
to["b1USvtdkLrXXtzTfz8R5tpicJYobDbwuqeT"] = 200
to["b1dSx5FTXEpzB7hWZAydY5N4A5PtFJb57V1"] = 300
to["b1Vc6vBWzjSp71c3c49hx3pENPL1TwU1Exy"] = 400


boxd.faucet(addr, amount)
time.sleep(3)


from boxd_client.signutils import calc_tx_hash_for_sig

unsigned_tx = boxd.make_unsigned_transaction(addr, to, fee)
for i in range(len(unsigned_tx.tx.vin)):
    vin = unsigned_tx.tx.vin[i]
    script_sig = vin.script_sig
    rawMsg = calc_tx_hash_for_sig(script_sig, unsigned_tx.tx, i)
    a = encode_hex(rawMsg)
    b = encode_hex(unsigned_tx.rawMsgs[i])
    print ( a)
    print ( b)
    print (a == b)


signed_tx = boxd.sign_unsigned_transaction(unsigned_tx.tx, priv_key_hex, unsigned_tx.rawMsgs)
ret = boxd.send_transaction(signed_tx)
time.sleep(1)

tx_detail = boxd.view_tx_detail(ret.hash , False)
print (tx_detail)


# 0x12260a240a2064124bd77d3c13cdd5b96ada70772f69cde96648c059b49bd6acf361ec771c95100112260a240a2064124bd77d3c13cdd5b96ada70772f69cde96648c059b49bd6acf361ec771c951004
# 1a1d0864121976a914014b73fa24ba03acb300c64ed12c0c4ebc06c25288ac1a1e08c801121976a91407056d0500e1c102bdb382c1339ed6f75db5ccc788ac1a1e08ac02121976a91469bf8ba2e9462d830a021a4748abc8c2afaac90288ac1a1e089003121976a91413b9aa477777c51603a2d5efb620d49faed1bd5c88ac1a1e088443121976a91407056d0500e1c102bdb382c1339ed6f75db5ccc788ac

# 0x12260a240a2064124bd77d3c13cdd5b96ada70772f69cde96648c059b49bd6acf361ec771c95100112410a240a2064124bd77d3c13cdd5b96ada70772f69cde96648c059b49bd6acf361ec771c951004
# 121976a91407056d0500e1c102bdb382c1339ed6f75db5ccc788ac1a1d0864121976a914014b73fa24ba03acb300c64ed12c0c4ebc06c25288ac1a1e08c801121976a91407056d0500e1c102bdb382c1339ed6f75db5ccc788ac1a1e08ac02121976a91469bf8ba2e9462d830a021a4748abc8c2afaac90288ac1a1e089003121976a91413b9aa477777c51603a2d5efb620d49faed1bd5c88ac1a1e088443121976a91407056d0500e1c102bdb382c1339ed6f75db5ccc788ac