#!/usr/bin/env python3
"""
Ransomware Educacional - Decrypter
Descriptografa arquivos previamente criptografados pelo encrypter.py.
Requer o arquivo key.key (chave) gerado durante a criptografia.
"""

import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

TARGET_DIR = "./test_files"
KEY_FILE = "key.key"

def load_key(filename):
    with open(filename, "rb") as f:
        return f.read()

def decrypt_file(encrypted_path, key):
    """
    Lê o IV (primeiros 16 bytes) e o ciphertext, descriptografa e restaura o arquivo original.
    """
    with open(encrypted_path, "rb") as f:
        iv = f.read(16)
        ciphertext = f.read()

    # Configura o cipher para descriptografia
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove o padding PKCS7
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Reconstrói o nome do arquivo original (remove a extensão .encrypted)
    original_path = encrypted_path[:-10]  # remove ".encrypted"
    with open(original_path, "wb") as f:
        f.write(plaintext)

    # Remove o arquivo criptografado
    os.remove(encrypted_path)

def main():
    if not os.path.exists(KEY_FILE):
        print("[ERRO] Arquivo key.key não encontrado. Não é possível descriptografar.")
        sys.exit(1)

    key = load_key(KEY_FILE)

    # Procura por todos os arquivos .encrypted na pasta alvo
    files_decrypted = False
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(".encrypted"):
            encrypted_path = os.path.join(TARGET_DIR, filename)
            print(f"[+] Descriptografando: {filename} -> {filename[:-10]}")
            decrypt_file(encrypted_path, key)
            files_decrypted = True

    if files_decrypted:
        print("[+] Todos os arquivos foram restaurados com sucesso!")
        # Opcional: remove o arquivo de chave após uso (em ransomware real não removem)
        # os.remove(KEY_FILE)
    else:
        print("[!] Nenhum arquivo .encrypted encontrado na pasta.")

if __name__ == "__main__":
    main()