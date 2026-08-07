from PIL import Image
import numpy as np
import os
from pathlib import Path
import time

# =========================================================
# CONFIGURAÇÕES
# =========================================================

# 19000 x 19000 RGB = ~1,08 GB de dados brutos
# Como os pixels são aleatórios, o PNG praticamente
# não conseguirá comprimir a imagem.
WIDTH = 19000
HEIGHT = 19000

# Descobre a Área de Trabalho
desktop = Path.home() / "Desktop"

# Caso o Windows esteja em português e use "Área de Trabalho"
if not desktop.exists():
    desktop = Path.home() / "Área de Trabalho"

output = desktop / "gigante_1GB.png"

print("=" * 60)
print("GERADOR DE PNG GIGANTE")
print("=" * 60)
print(f"Resolução: {WIDTH:,} x {HEIGHT:,}")
print(f"Pixels: {WIDTH * HEIGHT:,}")
print(f"Destino: {output}")
print()
print("Gerando pixels aleatórios...")
print("Isso pode consumir bastante RAM e demorar alguns minutos.")
print()

inicio = time.time()

# =========================================================
# GERAR IMAGEM
# =========================================================

# Gerador moderno do NumPy
rng = np.random.default_rng()

# Cria pixels RGB aleatórios
pixels = rng.integers(
    0,
    256,
    size=(HEIGHT, WIDTH, 3),
    dtype=np.uint8
)

print("Pixels gerados.")
print("Criando imagem...")

img = Image.fromarray(pixels, "RGB")

# Libera referência extra
del pixels

print("Salvando PNG...")
print("Não feche o programa.")

# compress_level=0:
# praticamente desativa a compressão DEFLATE,
# deixando o arquivo próximo do tamanho bruto.
img.save(
    output,
    format="PNG",
    compress_level=0
)

# =========================================================
# RESULTADO
# =========================================================

size_bytes = os.path.getsize(output)
size_mb = size_bytes / (1024 ** 2)
size_gb = size_bytes / (1024 ** 3)

tempo = time.time() - inicio

print()
print("=" * 60)
print("CONCLUÍDO")
print("=" * 60)
print(f"Arquivo: {output}")
print(f"Tamanho: {size_mb:.2f} MB")
print(f"Tamanho: {size_gb:.3f} GB")
print(f"Tempo: {tempo:.1f} segundos")
print("=" * 60)
