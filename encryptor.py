# מודול להצפנת קבצים ופענוחם באמצעות מפתח שמור.

from cryptography.fernet import Fernet
import os

def load_key():
    """
    טוען את המפתח הסימטרי מתוך הקובץ secret.key.
    """
    key_path = os.path.join(os.path.dirname(__file__), "secret.key")
    with open(key_path, "rb") as key_file:
        return key_file.read()

def encrypt_file(filepath):
    """
    מצפין קובץ נתון באמצעות Fernet ושומר אותו עם סיומת .enc.
    """
    key = load_key()
    fernet = Fernet(key)

    with open(filepath, "rb") as file:
        original_data = file.read()

    encrypted_data = fernet.encrypt(original_data)

    with open(filepath + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    print(f"[+] file '{filepath}' encrypted successfully as '{filepath}.enc'")

def decrypt_file(filepath):
    """
    מפענח קובץ מוצפן עם סיומת .enc ושומר אותו כקובץ מפוענח.
    """
    key = load_key()
    fernet = Fernet(key)

    with open(filepath, "rb") as enc_file:
        encrypted_data = enc_file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    base_name, ext = os.path.splitext(filepath)

    if ext == ".enc":
        base_name_without_enc, ext2 = os.path.splitext(base_name)
        new_path = f"{base_name_without_enc}_decrypted{ext2}"
    else:
        new_path = filepath + "_decrypted"

    with open(new_path, "wb") as dec_file:
        dec_file.write(decrypted_data)

    print(f"[+] file '{filepath}' decrypted successfully as '{new_path}'")

if __name__ == "__main__":
    mode = input("Encrypt or Decrypt? (e/d): ").strip().lower()
    path = input("Enter file path: ").strip()

    if mode == 'e':
        encrypt_file(path)
    elif mode == 'd':
        decrypt_file(path)
    else:
        print("Invalid option.")
