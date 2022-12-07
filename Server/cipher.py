import rsa

class Cipher:

    """ Constructor """
    def __init__(self):
        # Constant
        self._N_BITS = 1500
        # Make keys
        self.publicKey, self.privateKey = rsa.newkeys(self._N_BITS)
        self._max_msg = self._N_BITS // 8 - 11
        # Hold another public key for decryption
        self.encryptKey = None
        print(f"[CIPHER] Max msg length: {self._max_msg}")

    """ Update key used for encryption via string """
    def addKeyFromString(self, s : str):
        s = s.replace("(", "").replace(")", "").split(", ")
        for i in range(len(s)):
            s[i] = int(s[i])
        self.encryptKey = rsa.PublicKey(s[0], s[1])

    """ Returns this cipher's public key as string """
    def getPublicKey(self) -> str:
        return str(self.publicKey).replace("PublicKey", "")

    """ Decrypts a message using this cipher's private key """
    def decrypt(self, msg):
        return rsa.decrypt(msg, self.privateKey)

    """ Encrypts a message using previously stored public key """
    def encrypt(self, msg):
        return rsa.encrypt(msg, self.encryptKey)