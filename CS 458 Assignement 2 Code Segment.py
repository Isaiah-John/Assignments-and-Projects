# Substitution Ciphers
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

def permutation_cipher_encrypt(plaintext, permutation):
    encrypted = ''.join(plaintext[i] for i in permutation)
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
    first_transposition = simple_transposition_encrypt(plaintext, block_size)
    return simple_transposition_encrypt(first_transposition, block_size)

def double_transposition_decrypt(ciphertext, block_size):
    first_decryption = simple_transposition_decrypt(ciphertext, block_size)
    return simple_transposition_decrypt(first_decryption, block_size)


# Vigenère Cipher
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


# Main Program
def display_menu():
    print("\nChoose an encryption technique:")
    print("1. Shift Cipher")
    print("2. Permutation Cipher")
    print("3. Simple Transposition Cipher")
    print("4. Double Transposition Cipher")
    print("5. Vigenère Cipher")
    print("6. Exit")


def get_encryption_key():
    return input("Enter the encryption key: ")


def get_decryption_key(default_key):
    use_default = input(f"Do you want to use the default key '{default_key}' for decryption? (y/n): ").lower()
    if use_default == 'y':
        return default_key
    return input("Enter the decryption key: ")


def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':  # Shift Cipher
            plaintext = input("Enter the plaintext message: ")
            shift = int(input("Enter the shift value: "))
            key = input("Do you want to enter an encryption key? (y/n): ").lower()
            if key == 'y':
                shift = int(input("Enter the shift value: "))
            ciphertext = shift_cipher_encrypt(plaintext, shift)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decryption_key = get_decryption_key(str(shift))
                decrypted_message = shift_cipher_decrypt(ciphertext, int(decryption_key))
                print(f"Decrypted message: {decrypted_message}")

        elif choice == '2':  # Permutation Cipher
            plaintext = input("Enter the plaintext message: ")
            permutation = list(map(int, input("Enter the permutation indices (space-separated): ").split()))
            key = input("Do you want to enter an encryption key? (y/n): ").lower()
            if key == 'y':
                permutation = list(map(int, input("Enter the permutation indices (space-separated): ").split()))
            ciphertext = permutation_cipher_encrypt(plaintext, permutation)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decryption_key = get_decryption_key(str(permutation))
                decrypted_message = permutation_cipher_decrypt(ciphertext, list(map(int, decryption_key.split())))
                print(f"Decrypted message: {decrypted_message}")

        elif choice == '3':  # Simple Transposition Cipher
            plaintext = input("Enter the plaintext message: ")
            block_size = int(input("Enter the block size: "))
            key = input("Do you want to enter an encryption key? (y/n): ").lower()
            if key == 'y':
                block_size = int(input("Enter the block size: "))
            ciphertext = simple_transposition_encrypt(plaintext, block_size)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decryption_key = get_decryption_key(str(block_size))
                decrypted_message = simple_transposition_decrypt(ciphertext, int(decryption_key))
                print(f"Decrypted message: {decrypted_message}")

        elif choice == '4':  # Double Transposition Cipher
            plaintext = input("Enter the plaintext message: ")
            block_size = int(input("Enter the block size: "))
            key = input("Do you want to enter an encryption key? (y/n): ").lower()
            if key == 'y':
                block_size = int(input("Enter the block size: "))
            ciphertext = double_transposition_encrypt(plaintext, block_size)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decryption_key = get_decryption_key(str(block_size))
                decrypted_message = double_transposition_decrypt(ciphertext, int(decryption_key))
                print(f"Decrypted message: {decrypted_message}")

        elif choice == '5':  # Vigenère Cipher
            plaintext = input("Enter the plaintext message: ")
            key = input("Enter the encryption key: ")
            ciphertext = vigenere_cipher_encrypt(plaintext, key)
            print(f"Encrypted message: {ciphertext}")
            decrypt_choice = input("Do you want to decrypt? (y/n): ").lower()
            if decrypt_choice == 'y':
                decryption_key = get_decryption_key(key)
                decrypted_message = vigenere_cipher_decrypt(ciphertext, decryption_key)
                print(f"Decrypted message: {decrypted_message}")

        elif choice == '6':  # Exit
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
