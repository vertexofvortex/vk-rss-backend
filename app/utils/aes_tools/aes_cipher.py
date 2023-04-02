import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


class AESTools():
    def encrypt(self, raw_value, raw_key):
        value = self._pad(raw_value)
        key = hashlib.sha256(raw_key.encode()).digest()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        return base64.b64encode(iv + cipher.encrypt(value.encode()))
    
    def decrypt(self, enc_value, raw_key):
        value = base64.b64decode(enc_value)
        key = hashlib.sha256(raw_key.encode()).digest()
        iv = value[: AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)

        return self._unpad(cipher.decrypt(value[AES.block_size :])).decode("utf-8")

    @staticmethod
    def _pad(s):
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
    
    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]
    
aes_tools = AESTools()