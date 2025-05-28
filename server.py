# שרת TCP לקבלת קבצים מוצפנים מהמחשב המרוחק, שמירתם בתיקייה מקומית, פענוח ומחיקת הקובץ המוצפן.

import socket
import threading
import os
from encryptor import decrypt_file  # ייבוא פונקציית הפענוח

HOST = '127.0.0.1'
PORT = 5000
DEST_FOLDER = 'received_files'

def handle_client(conn, addr):
    """
    מטפל בחיבור מלקוח: מקבל שם קובץ, שומר את תוכנו, מפענח אותו אם צריך ומוחק את הגרסה המוצפנת.
    """
    print(f"[+] Connection from {addr}")
    try:
        raw_length = conn.recv(4)
        if len(raw_length) < 4:
            raise ValueError("Invalid filename length received.")

        filename_length = int.from_bytes(raw_length, 'big')

        filename_bytes = b''
        while len(filename_bytes) < filename_length:
            chunk = conn.recv(filename_length - len(filename_bytes))
            if not chunk:
                raise ValueError("Filename reception interrupted.")
            filename_bytes += chunk

        relative_path = filename_bytes.decode()
        save_path = os.path.join(DEST_FOLDER, relative_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)

        print(f"[+] Saved encrypted file: {save_path}")

        if save_path.endswith(".enc"):
            decrypt_file(save_path)
            try:
                os.remove(save_path)
                print(f"[+] Deleted encrypted file: {save_path}")
            except Exception as e:
                print(f"[-] Failed to delete encrypted file {save_path}: {e}")

    except Exception as e:
        print(f"[-] Error with {addr}: {e}")
    finally:
        conn.close()

def start_server():
    """
    מפעיל את השרת ומאזין לחיבורים נכנסים.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[+] Server listening on port {PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
