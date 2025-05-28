from cryptography.fernet import Fernet

def generate_key():#הפונקציה יוצרת מפתח הצפנה סימטרי חדש
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    print(f'Key generated and saved to secret.key')

if __name__ == '__main__':
    generate_key()