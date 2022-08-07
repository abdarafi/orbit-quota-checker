import base64, hashlib, random

def code_verifier():
    return base64.b64encode(random.randbytes(50)).decode('utf-8').replace("+", "-").replace("/", "_").replace("=", "") 

def code_challenge(code_verifier):
    return base64.b64encode(hashlib.sha256(bytes(code_verifier, encoding='utf8')).digest()).decode('utf-8').replace("+", "-").replace("/", "_").replace("=", "")