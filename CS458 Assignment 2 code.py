from Crypto.Cipher import AES, DES, DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import DES3
import base64

########################################################################################################################

# Cipher Functions #

# Vigenère Encrypt and Decrypt
def vigenere_cipher_encrypt(plaintext, key):
    key = key.lower()
    ciphertext = ""
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            if char.isupper():
                ciphertext += chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                ciphertext += chr((ord(char) - 97 + shift) % 26 + 97)
            key_index += 1
        else:
            ciphertext += char
    return ciphertext

def vigenere_cipher_decrypt(ciphertext, key):
    key = key.lower()
    plaintext = ""
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('a')
            if char.isupper():
                plaintext += chr((ord(char) - 65 - shift) % 26 + 65)
            else:
                plaintext += chr((ord(char) - 97 - shift) % 26 + 97)
            key_index += 1
        else:
            plaintext += char
    return plaintext    

# Shift Cipher
def shift_cipher_encrypt(plaintext, shift):
    encrypted = ""
    for char in plaintext:
        if char.isalpha():
            shift_amount = 65 if char.isupper() else 97
            encrypted += chr((ord(char) - shift_amount + shift) % 26 + shift_amount)
        else:
            encrypted += char
    return encrypted

def shift_cipher_decrypt(ciphertext, shift):
    return shift_cipher_encrypt(ciphertext, -shift)

# Permutation Cipher                
def permutation_cipher_encrypt(plaintext, permutation):
    encrypted = ''.join(plaintext[i] if i < len(plaintext) else '' for i in permutation)
    return encrypted

def permutation_cipher_decrypt(ciphertext, permutation):
    decrypted = [''] * len(ciphertext)
    for i, char in enumerate(ciphertext):
        decrypted[permutation[i]] = char
    return ''.join(decrypted)

# Transposition Ciphers
def simple_transposition_encrypt(plaintext, block_size):
    ciphertext = ''
    for i in range(0, len(plaintext), block_size):
        ciphertext += plaintext[i:i+block_size][::-1]  # Reverse the block
    return ciphertext

def simple_transposition_decrypt(ciphertext, block_size):
    plaintext = ''
    for i in range(0, len(ciphertext), block_size):
        plaintext += ciphertext[i:i+block_size][::-1]  # Reverse the block back
    return plaintext

def double_transposition_encrypt(plaintext, block_size):
    rows = len(plaintext) // block_size
    columns = block_size
    matrix = [[' ' for _ in range(columns)] for _ in range(rows)]
    index = 0
    for column in range(columns):
        for row in range(rows):
            matrix[row][column] = plaintext[index]
            index += 1
    ciphertext = ''
    for row in range(rows):
        for column in range(columns):
            ciphertext += matrix[row][column]
    return ciphertext

def double_transposition_decrypt(ciphertext, block_size):
    rows = len(ciphertext) // block_size
    columns = block_size
    matrix = [[' ' for _ in range(columns)] for _ in range(rows)]
    index = 0
    for row in range(rows):
        for column in range(columns):
            matrix[row][column] = ciphertext[index]
            index += 1
    plaintext = ''
    for column in range(columns):
        for row in range(rows):
            plaintext += matrix[row][column]
    return plaintext

########################################################################################################################

# AES, DES, 3DES Encryption and Decryption with Modes
def aes_encrypt(plaintext, key, mode):
    cipher = AES.new(key, mode)
    padded_data = pad(plaintext.encode(), AES.block_size)  # Pad the plaintext to block size
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

def aes_decrypt(ciphertext, key, mode):
    cipher = AES.new(key, mode)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)  # Remove padding
    return decrypted_data.decode()

def des_encrypt(plaintext, key, mode):
    cipher = DES.new(key, mode)
    padded_data = pad(plaintext.encode(), DES.block_size)  # Pad the plaintext to block size
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

def des_decrypt(ciphertext, key, mode):
    cipher = DES.new(key, mode)
    decrypted_data = unpad(cipher.decrypt(ciphertext), DES.block_size)  # Remove padding
    return decrypted_data.decode('utf-8', errors='ignore')  # Handle binary data properly

def des3_encrypt(plaintext, key, mode):
    cipher = DES3.new(key, mode)
    padded_data = pad(plaintext.encode(), DES3.block_size)  # Pad the plaintext to block size
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

def des3_decrypt(ciphertext, key, mode):
    cipher = DES3.new(key, mode)
    decrypted_data = unpad(cipher.decrypt(ciphertext), DES3.block_size)  # Remove padding
    return decrypted_data.decode('utf-8', errors='ignore')  # Handle binary data properly

########################################################################################################################

# Menu Code #
def main_menu():
    print("\nEncryption Time!\nChoose an encryption method:")
    print("1. Substitution Ciphers")
    print("2. Transposition Ciphers")
    print("3. Vigenère Cipher")
    print("4. AES Encryption (AES-128)")
    print("5. DES Encryption (DES-56)")
    print("6. 3DES Encryption (DES-168)")
    print("7. Exit")

def sub_menu():
    print("\nChoose a Substitution Encryption Technique")
    print("1. Shift Cipher")
    print("2. Permutation Cipher")
    print("3. Back")
    print("4. Exit")

def tran_menu():
    print("\nChoose a Transposition Encryption Technique")
    print("1. Simple Transposition Cipher")
    print("2. Double Transposition Cipher")
    print("3. Back")
    print("4. Exit")

def aes_menu():
    print("\nChoose AES encryption mode:")
    print("1. ECB")
    print("2. CBC")
    print("3. CFB")
    print("4. OFB")

def des_menu():
    print("\nChoose DES encryption mode:")
    print("1. ECB")
    print("2. CBC")
    print("3. CFB")
    print("4. OFB")

def des3_menu():
    print("\nChoose 3DES encryption mode:")
    print("1. ECB")
    print("2. CBC")
    print("3. CFB")
    print("4. OFB")

def wrong_input():
    print("Incorrect value chosen! Please put in a correct value!")

########################################################################################################################

# Tool Functions
def get_encryption_key():
    return input("Enter the encryption key (16 bytes for AES-128, 8 bytes for DES, 24 bytes for 3DES): ")

def get_decryption_key(default_key):
    use_default = input(f"Do you want to use the default key '{default_key}' for decryption? (y/n): ").lower()
    if use_default == 'y':
        return default_key
    return input("Enter the decryption key: ")

########################################################################################################################

# Main Body
def main():
    while True:
        main_menu()
        cipherChoice = input("Enter your choice: ")

        if cipherChoice == '1':  # Substitution Ciphers
            sub_menu()
            cipherChoice = input("Enter your choice: ")
            
            if cipherChoice == '1':  # Shift Cipher
                plaintext = input("Enter the plaintext message: ")
                shift = int(input("Enter the shift value: "))
                ciphertext = shift_cipher_encrypt(plaintext, shift)
                print(f"Encrypted message: {ciphertext}")
                decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
                if decrypt_choice == 'y':
                    decrypted_message = shift_cipher_decrypt(ciphertext, shift)
                    print(f"Decrypted message: {decrypted_message}")

            elif cipherChoice == '2':  # Permutation Cipher
                plaintext = input("Enter the plaintext message: ")
                permutation = list(map(int, input("Enter the permutation indices (space-separated): ").split()))
                ciphertext = permutation_cipher_encrypt(plaintext, permutation)
                print(f"Encrypted message: {ciphertext}")
                decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
                if decrypt_choice == 'y':
                    decrypted_message = permutation_cipher_decrypt(ciphertext, permutation)
                    print(f"Decrypted message: {decrypted_message}")

            elif cipherChoice == '3':  # Return to main menu
                continue

            elif cipherChoice == '4':  # Exit
                break
            else:
                wrong_input()

        elif cipherChoice == '2':  # Transposition Ciphers
            tran_menu()
            cipherChoice = input("Enter your choice: ")
            
            if cipherChoice == '1':  # Simple Transposition Cipher
                plaintext = input("Enter the plaintext message: ")
                block_size = int(input("Enter the block size: "))
                ciphertext = simple_transposition_encrypt(plaintext, block_size)
                print(f"Encrypted message: {ciphertext}")
                decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
                if decrypt_choice == 'y':
                    decrypted_message = simple_transposition_decrypt(ciphertext, block_size)
                    print(f"Decrypted message: {decrypted_message}")

            elif cipherChoice == '2':  # Double Transposition Cipher
                plaintext = input("Enter the plaintext message: ")
                block_size = int(input("Enter the block size: "))
                ciphertext = double_transposition_encrypt(plaintext, block_size)
                print(f"Encrypted message: {ciphertext}")
                decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
                if decrypt_choice == 'y':
                    decrypted_message = double_transposition_decrypt(ciphertext, block_size)
                    print(f"Decrypted message: {decrypted_message}")

            elif cipherChoice == '3':  # Return to main menu
                continue

            elif cipherChoice == '4':  # Exit
                break
            else:
                wrong_input()

        elif cipherChoice == '3':  # Vigenère Cipher
            plaintext = input("Enter the plaintext message: ")
            key = input("Enter the encryption key: ")
            ciphertext = vigenere_cipher_encrypt(plaintext, key)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decrypted_message = vigenere_cipher_decrypt(ciphertext, key)
                print(f"Decrypted message: {decrypted_message}")

        elif cipherChoice == '4':  # AES Encryption (AES-128)
            key = get_encryption_key().encode('utf-8')
            aes_menu()
            mode_choice = int(input("Enter your choice: "))
            mode = [AES.MODE_ECB, AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB][mode_choice - 1]
            plaintext = input("Enter the plaintext message: ")
            ciphertext = aes_encrypt(plaintext, key, mode)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decrypted_message = aes_decrypt(ciphertext, key, mode)
                print(f"Decrypted message: {decrypted_message}")

        elif cipherChoice == '5':  # DES Encryption (DES-56)
            key = get_encryption_key().encode('utf-8')
            des_menu()
            mode_choice = int(input("Enter your choice: "))
            mode = [DES.MODE_ECB, DES.MODE_CBC, DES.MODE_CFB, DES.MODE_OFB][mode_choice - 1]
            plaintext = input("Enter the plaintext message: ")
            ciphertext = des_encrypt(plaintext, key, mode)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decrypted_message = des_decrypt(ciphertext, key, mode)
                print(f"Decrypted message: {decrypted_message}")

        elif cipherChoice == '6':  # 3DES Encryption (DES-168)
            key = get_encryption_key().encode('utf-8')
            des3_menu()
            mode_choice = int(input("Enter your choice: "))
            mode = [DES3.MODE_ECB, DES3.MODE_CBC, DES3.MODE_CFB, DES3.MODE_OFB][mode_choice - 1]
            plaintext = input("Enter the plaintext message: ")
            ciphertext = des3_encrypt(plaintext, key, mode)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decrypted_message = des3_decrypt(ciphertext, key, mode)
                print(f"Decrypted message: {decrypted_message}")

        elif cipherChoice == '7':  # Return to main menu
            print("Program Ended. Goodbye!")
            break



if __name__ == "__main__":
    main()

