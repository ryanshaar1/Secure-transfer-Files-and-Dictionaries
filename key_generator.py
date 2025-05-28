# סקריפט ליצירת מפתח הצפנה סימטרי ושמירתו בקובץ בשם secret.key

from cryptography.fernet import Fernet

def generate_key():
    """
    מייצר מפתח הצפנה חדש ושומר אותו בקובץ secret.key.
    """
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    print(f'Key generated and saved to secret.key')

if __name__ == '__main__':
    generate_key()
