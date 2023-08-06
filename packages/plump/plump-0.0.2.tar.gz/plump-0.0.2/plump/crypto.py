import rsa
from binascii import a2b_hex, b2a_hex
from pyDes import des, PAD_PKCS5, ECB

############################# RSA #################################
class RsaUtils(object):
    def __init__(self,e,m):
        self.e = e
        self.m = m

    def encrypt(self,message):
        mm = int(self.m, 16)
        ee = int(self.e, 16)
        rsa_pubkey = rsa.PublicKey(mm, ee)
        out = self._encrypt(message.encode(), rsa_pubkey)
        return out.hex()

    def _pad_for_encryption(self, message, target_length):
        message = message[::-1]
        max_msglength = target_length - 11
        msglength = len(message)

        padding = b''
        padding_length = target_length - msglength - 3

        for i in range(padding_length):
            padding += b'\x00'

        return b''.join([b'\x00\x00',padding,b'\x00',message])

    def _encrypt(self, message, pub_key):
        keylength = rsa.common.byte_size(pub_key.n)
        padded = self._pad_for_encryption(message, keylength)

        payload = rsa.transform.bytes2int(padded)
        encrypted = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
        block = rsa.transform.int2bytes(encrypted, keylength)

        return block

def rsa_encrypt(e,m,message):
    return RsaUtils(e,m).encrypt(message)


############################# DES #################################
class DesUtils(object):
    def __init__(self, secret):
        self.__iv = '\x00'*8
        self._secret = secret
        self._des = None
        self._initdes()

    def _initdes(self):
        secret_length = len(self._secret)
        if secret_length < 8:
            self._secret = self._secret + '\x00' * (8 - secret_length)
        else:
            self._secret = self._secret[:8]

        self._des = des(self._secret, ECB, self.__iv, pad=None, padmode=PAD_PKCS5)

    # 加密
    def encrypt(self, strin):
        en = self._des.encrypt(strin, padmode=PAD_PKCS5)
        return b2a_hex(en).decode('utf-8')

    # 解密
    def decrypt(self, strin):
        de = self._des.decrypt(a2b_hex(strin), padmode=PAD_PKCS5)
        return de.decode('utf-8')

def des_encrypt(secret,strin):
    return DesUtils(secret).encrypt(strin)

def des_decrypt(secret,strin):
    return DesUtils(secret).decrypt(strin)