"""
Credit to: https://blog.miguelgrinberg.com/post/json-web-tokens-with-public-key-signatures
I have added additional examples on signature verification on modified signature and payload
"""

import base64
import jwt
import json

secret_key = "very strong secret"
# encode return as bytes
token = jwt.encode({"user": "hello"}, secret_key, algorithm='HS256').decode('utf-8')
print("Encode message using HS256:", token)

# Using private key (this can be generated using ssh-keygen command)
private_key = open("C:\\tools\\cert\\id_rsa").read()
token = jwt.encode({"user": "hello"}, private_key, algorithm="RS256").decode('utf-8')
print("Generated with RS256:", token)

# End user can decode with the public key but cannot generate JWT since the private key is not known
public_key = open("C:\\tools\\cert\\id_rsa.pub").read()
payload = jwt.decode(token, public_key, algorithms="RS256", verify=True)
print("Decode JWT with Public key:", payload)

# Tamper signature in token and check if the Signature verification works
try:
    tampered_token = token + "ABCDE"
    payload = jwt.decode(tampered_token, public_key, algorithms="RS256", verify=True)
except jwt.exceptions.PyJWTError as err:
    print("[Tamper Signature] Encounter error during decoding:", err)

# Generate a modified payload
payload = json.dumps({"user": "hello123"}, separators=(',', ':')).encode('utf-8')
new_payload = base64.urlsafe_b64encode(payload).replace(b'=', b'').decode('utf-8')
print(new_payload)
token_arr = token.split(".")

# Tamper payload in the token and verify signature. We expect the Signature verification to fail
try:
    tampered_token2 = token_arr[0] + "." + new_payload + "." + token_arr[2]
    payload = jwt.decode(tampered_token2, public_key, algorithms="RS256", verify=True)
except jwt.exceptions.PyJWTError as err:
    print("[Tamper Payload] Encounter error during decoding:", err)
