# לקוח לשליחת קבצים לשרת: מצפין קבצים, שולח אותם דרך סוקט, מוחק את הגרסה המוצפנת לאחר השליחה.

import socket
import os
from concurrent.futures import ThreadPoolExecutor
from encryptor import encrypt_file

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
MAX_THREADS = 5

def send_file(full_path, base_folder):
    """
    מצפין קובץ, יוצר סוקט ומעביר אותו לשרת, ואז מוחק את הקובץ המוצפן.
    """
    print(f"[DEBUG] Starting send_file for {full_path}")

    relative_path = os.path.relpath(full_path, base_folder)

    try:
        encrypt_file(full_path)
        encrypted_path = full_path + ".enc"
        encrypted_relative_path = relative_path + ".enc"

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))

        filename_bytes = encrypted_relative_path.encode()
        filename_length = len(filename_bytes)
        client.send(filename_length.to_bytes(4, 'big'))
        client.send(filename_bytes)

        with open(encrypted_path, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client.send(data)

        client.close()
        print(f"[+] Sent: {encrypted_relative_path}")

    except Exception as e:
        print(f"[-] Failed in send_file for {full_path}: {e}")

    finally:
        if os.path.exists(full_path + ".enc"):
            try:
                os.remove(full_path + ".enc")
            except Exception as e:
                print(f"[-] Failed to delete encrypted file: {e}")

def cleanup_old_encrypted_files(folder_path):
    """
    מוחק קבצים מוצפנים ישנים שנותרו בתיקייה.
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".enc"):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"[-] Failed to delete old encrypted file {file}: {e}")

def send_directory(folder_path):
    """
    שולח את כל הקבצים בתיקייה בצורה מרובת־תהליכים.
    """
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        if "__pycache__" in root:
            continue
        for file in files:
            if file.endswith(".enc"):
                continue
            full_path = os.path.join(root, file)
            all_files.append(full_path)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(lambda f: send_file(f, folder_path), all_files)

if __name__ == "__main__":
    folder = input("Enter folder path to send: ")
    if os.path.isdir(folder):
        cleanup_old_encrypted_files(folder)
        send_directory(folder)
    else:
        print("[-] Folder does not exist.")
