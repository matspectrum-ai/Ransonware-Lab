
# 💀 Ransomware Educacional em Python – AES-256-CBC

> **ATENÇÃO:** Este projeto é **estritamente educacional**. Desenvolvido para entender o funcionamento de ransomware, aprender criptografia simétrica e práticas de resposta a incidentes. **Não utilize fora de laboratório autorizado.**

## 🎯 Objetivo

Implementar um ransomware didático que:
- Criptografa arquivos de uma pasta de teste usando AES-256 no modo CBC.
- Gera uma chave aleatória e a salva localmente (em um cenário real, o atacante a enviaria para um servidor C2).
- Oferece um descriptografador que restaura os arquivos originais (simulando a ação de pagamento do resgate).

## ⚙️ Como funciona (alto nível)

1. **encrypter.py** – percorre todos os arquivos em `./test_files/`, gera uma chave AES-256, criptografa cada arquivo (salvando o IV junto) e apaga o original.
2. **decrypter.py** – lê a chave (`key.key`), localiza os arquivos com extensão `.encrypted`, restaura o conteúdo original e remove os arquivos criptografados.

## 🧪 Ambiente de teste recomendado

| Componente        | Especificação                                      |
|-------------------|----------------------------------------------------|
| SO                | Kali Linux / Ubuntu / Windows WSL2 / VM isolada    |
| Python            | 3.8+                                               |
| Biblioteca        | `cryptography` (instale com `pip install cryptography`) |
| Pasta alvo        | Criar `./test_files/` com alguns arquivos .txt, .jpg, .pdf |

## 🚀 Execução passo a passo (laboratório)

### 1. Preparação

```bash
mkdir test_files
echo "Conteúdo secreto" > test_files/documento.txt
cp imagem.png test_files/   # (opcional)
pip install cryptography
```

2. Criptografar (simulando ataque)

```bash
python3 encrypter.py
```

Saída esperada:

```
[+] Chave gerada e salva em key.key (guarde com segurança!)
[+] Criptografando: documento.txt
[+] Todos os arquivos foram criptografados.
```

A pasta test_files/ agora contém documento.txt.encrypted e o original sumiu.

3. Descriptografar (simulando resgate)

```bash
python3 decrypter.py
```

Saída:

```
[+] Descriptografando: documento.txt.encrypted -> documento.txt
[+] Todos os arquivos foram restaurados com sucesso!
```

Arquivo original recuperado.

📸 Evidências (pasta /images)

1. antes_cripto.png – Conteúdo da pasta test_files antes.
2. depois_cripto.png – Após encrypter.py (arquivos .encrypted).
3. restaurado.png – Após decrypter.py (arquivos originais de volta).

🧠 Análise técnica – por dentro do código

Criptografia AES-256-CBC

· Chave: 32 bytes aleatórios (256 bits). Se o atacante perder a chave, os dados são irrecuperáveis.
· IV (Vetor de Inicialização): 16 bytes aleatórios, armazenado junto com o ciphertext. Garante que mesmo arquivos idênticos gerem saídas diferentes.
· Padding PKCS7: Necessário porque AES opera em blocos de 16 bytes. O padding adiciona bytes ao final para alinhar.
· Modo CBC: Cada bloco de texto cifrado depende do anterior – seguro contra ataques de repetição, mas requer IV aleatório.

Pontos fracos desta implementação (didáticos)

· A chave fica salva localmente (no mundo real, seria enviada para um servidor remoto).
· Não há persistência ou escalonamento de privilégios.
· Não criptografa recursivamente subpastas (poderia ser adicionado com os.walk).
· Não altera o nome dos arquivos (ransomwares reais muitas vezes renomeiam).

Como um ransomware real melhoraria?

· Comunicação C2: Enviar chave para um servidor remoto, exigindo pagamento para obtê-la.
· Exclusão segura: Sobrescrever os arquivos originais antes de deletar.
· Controle de chave por vítima: Gerar um par RSA para que apenas o atacante possa descriptografar.
· Anti-análise: Detectar sandbox, atrasar execução, ofuscar código.

🛡️ Defesas contra ransomware (Blue Team)

Contramedida Descrição
Backups offline (3-2-1) Cópias em mídia desconectada ou imutável (AWS S3 Object Lock, fita).
Controle de execução de scripts Restringir execução de Python/PowerShell não assinados (AppLocker, SELinux)
Monitoramento de renomeação em massa Ferramentas como Sysmon detectam mudanças extensas em extensões de arquivo.
Princípio do menor privilégio O ransomware roda com permissões do usuário – se ele não tiver acesso a backups, não os criptografa.
EDR / Antivírus comportamental Detecta padrões como encrypt_file + delete_original.

📚 Referências

· Cryptography.io – documentação oficial
· OWASP Ransomware
· NIST SP 800-38A – Modos de operação AES

👤 Autor

Desafio Formação Cibersegurança – DIO
Implementação adaptada e documentada por [Samara Meireles Sampaio de Sousa]
Data: Junho/2026

Use o conhecimento para proteger, nunca para atacar.
