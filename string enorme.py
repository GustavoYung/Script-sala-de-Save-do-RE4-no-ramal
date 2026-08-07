import subprocess

# ==========================================
# CONFIGURAÇÃO
# ==========================================

# Quantidade de caracteres
TAMANHO = 1_000_000

# Gera a string
texto = "A" * TAMANHO

print(f"Gerando {TAMANHO:,} caracteres...")

# ==========================================
# COPIA PARA O CTRL + V DO WINDOWS
# ==========================================

process = subprocess.Popen(
    ["clip"],
    stdin=subprocess.PIPE,
    text=True
)

process.communicate(texto)

print()
print("=" * 50)
print("COPIADO!")
print("=" * 50)
print(f"{TAMANHO:,} caracteres estão no Ctrl + V.")
print()
print("Agora abra o campo do seu site e pressione:")
print("CTRL + V")
print("=" * 50)

input("\nPressione ENTER para fechar...")
