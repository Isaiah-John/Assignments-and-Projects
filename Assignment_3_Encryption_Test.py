import unittest
from Crypto.Cipher import AES, DES, DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
# Import encryption methods from your main program
from Assignment_3_Encryption_Code import (
    shift_cipher_encrypt,
    shift_cipher_decrypt,
    permutation_cipher_encrypt,
    permutation_cipher_decrypt,
    vigenere_cipher_encrypt,
    vigenere_cipher_decrypt,
    simple_transposition_encrypt,
    simple_transposition_decrypt,
    double_transposition_encrypt,
    double_transposition_decrypt,
    aes_encrypt,
    aes_decrypt,
    des_encrypt,
    des_decrypt,
    des3_encrypt,
    des3_decrypt,
)

class TestEncryptionMethods(unittest.TestCase):

    def test_shift_cipher(self):
        plaintext = "Hello World!"
        shift = 3
        encrypted = shift_cipher_encrypt(plaintext, shift)
        decrypted = shift_cipher_decrypt(encrypted, shift)
        self.assertEqual(decrypted, plaintext, f"Failed for Shift Cipher. Expected {plaintext}, got {decrypted}")

    def test_permutation_cipher(self):
        plaintext = "Hello World"
        permutation = [3, 1, 4, 0, 2, 5, 8, 7, 6, 9, 10]
        encrypted = permutation_cipher_encrypt(plaintext, permutation)
        decrypted = permutation_cipher_decrypt(encrypted, permutation)
        self.assertEqual(decrypted, plaintext, f"Failed for Permutation Cipher. Expected {plaintext}, got {decrypted}")

    def test_vigenere_cipher(self):
        plaintext = "Hello World!"
        key = "key"
        encrypted = vigenere_cipher_encrypt(plaintext, key)
        decrypted = vigenere_cipher_decrypt(encrypted, key)
        self.assertEqual(decrypted, plaintext, f"Failed for Vigenère Cipher. Expected {plaintext}, got {decrypted}")

    def test_simple_transposition(self):
        plaintext = "Hello World!"
        block_size = 4
        encrypted = simple_transposition_encrypt(plaintext, block_size)
        decrypted = simple_transposition_decrypt(encrypted, block_size)
        self.assertEqual(decrypted, plaintext, f"Failed for Simple Transposition. Expected {plaintext}, got {decrypted}")

    def test_double_transposition(self):
        plaintext = "Hello World!"
        block_size = 4
        encrypted = double_transposition_encrypt(plaintext, block_size)
        decrypted = double_transposition_decrypt(encrypted, block_size)
        self.assertEqual(decrypted, plaintext, f"Failed for Double Transposition. Expected {plaintext}, got {decrypted}")

    def test_aes_encryption(self):
        key = get_random_bytes(16)  # AES-128 key (16 bytes)
        plaintext = "Hello World!"
        aes_modes = [AES.MODE_ECB, AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB]

        for mode in aes_modes:
            encrypted = aes_encrypt(plaintext, key, mode)
            decrypted = aes_decrypt(encrypted, key, mode)
            self.assertEqual(decrypted, plaintext, f"Failed for AES with mode {mode}. Expected {plaintext}, got {decrypted}")

    def test_des_encryption(self):
        key = get_random_bytes(8)  # DES key (8 bytes)
        plaintext = "Hello World!"
        des_modes = [DES.MODE_ECB, DES.MODE_CBC, DES.MODE_CFB, DES.MODE_OFB]

        for mode in des_modes:
            encrypted = des_encrypt(plaintext, key, mode)
            decrypted = des_decrypt(encrypted, key, mode)
            self.assertEqual(decrypted, plaintext, f"Failed for DES with mode {mode}. Expected {plaintext}, got {decrypted}")

    def test_des3_encryption(self):
        key = get_random_bytes(24)  # 3DES key (24 bytes)
        plaintext = "Hello World!"
        des3_modes = [DES3.MODE_ECB, DES3.MODE_CBC, DES3.MODE_CFB, DES3.MODE_OFB]

        for mode in des3_modes:
            encrypted = des3_encrypt(plaintext, key, mode)
            decrypted = des3_decrypt(encrypted, key, mode)
            self.assertEqual(decrypted, plaintext, f"Failed for 3DES with mode {mode}. Expected {plaintext}, got {decrypted}")

if __name__ == "__main__":
    unittest.main()
