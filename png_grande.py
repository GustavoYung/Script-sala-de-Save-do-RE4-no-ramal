from PIL import Image
from pathlib import Path
import os
import struct
import zlib

# =========================================================
# CONFIG
# =========================================================

TARGET_GB = 5
TARGET_SIZE = TARGET_GB * 1024 * 1024 * 1024

WIDTH = 4000
HEIGHT = 4000

desktop = Path.home() / "Desktop"

if not desktop.exists():
    desktop = Path.home() / "Área de Trabalho"

output = desktop / "gigante_5GB.png"

print("=" * 60)
print("CRIADOR DE PNG GIGANTE")
print("=" * 60)
print(f"Tamanho alvo: {TARGET_GB} GB")
print(f"Arquivo: {output}")
print()

# =========================================================
# CRIA PNG PRETO NORMAL
# =========================================================

print("Criando imagem preta...")

img = Image.new(
    "RGB",
    (WIDTH, HEIGHT),
    color="black"
)

img.save(
    output,
    format="PNG",
    compress_level=9
)

initial_size = os.path.getsize(output)

print(
    f"PNG base criado: "
    f"{initial_size / 1024 / 1024:.2f} MB"
)

# =========================================================
# LOCALIZA IEND
# =========================================================

with open(output, "rb") as f:
    png_data = f.read()

# PNG termina com este chunk
iend_signature = b"\x00\x00\x00\x00IEND\xaeB`\x82"

iend_position = png_data.rfind(iend_signature)

if iend_position == -1:
    raise RuntimeError("Chunk IEND não encontrado.")

before_iend = png_data[:iend_position]
iend = png_data[iend_position:]

# não precisamos mais manter tudo
del png_data

# =========================================================
# FUNÇÃO PARA CRIAR CHUNK PNG
# =========================================================

def create_chunk(chunk_type, data):
    length = struct.pack(">I", len(data))

    crc = zlib.crc32(chunk_type)
    crc = zlib.crc32(data, crc)
    crc = struct.pack(">I", crc & 0xffffffff)

    return (
        length +
        chunk_type +
        data +
        crc
    )

# =========================================================
# REESCREVE ARQUIVO
# =========================================================

print()
print("Expandindo arquivo para 5 GB...")
print("Isso não exige vários GB de RAM.")
print()

temp_output = desktop / "gigante_temp.png"

with open(temp_output, "wb") as out:

    out.write(before_iend)

    current_size = len(before_iend)

    # cada chunk terá 64 MB
    CHUNK_DATA_SIZE = 64 * 1024 * 1024

    counter = 0

    while True:

        # 12 bytes de overhead por chunk
        remaining = TARGET_SIZE - current_size - len(iend)

        if remaining <= 12:
            break

        data_size = min(
            CHUNK_DATA_SIZE,
            remaining - 12
        )

        if data_size <= 0:
            break

        # chunk privado
        chunk_type = b"ruSt"

        data = b"\x00" * data_size

        chunk = create_chunk(
            chunk_type,
            data
        )

        out.write(chunk)

        current_size += len(chunk)

        counter += 1

        gb_written = current_size / (1024 ** 3)

        print(
            f"\rGravado: "
            f"{gb_written:.2f} / "
            f"{TARGET_GB:.2f} GB",
            end=""
        )

    # ajuste final
    remaining = TARGET_SIZE - current_size - len(iend)

    if remaining >= 12:

        data_size = remaining - 12

        chunk = create_chunk(
            b"ruSt",
            b"\x00" * data_size
        )

        out.write(chunk)

    out.write(iend)

print()

# remove original
os.remove(output)

# renomeia temporário
os.rename(
    temp_output,
    output
)

# =========================================================
# RESULTADO
# =========================================================

final_size = os.path.getsize(output)

print()
print("=" * 60)
print("CONCLUÍDO")
print("=" * 60)

print(
    f"Arquivo: {output}"
)

print(
    f"Tamanho em bytes: "
    f"{final_size:,}"
)

print(
    f"Tamanho em GB: "
    f"{final_size / (1024**3):.4f} GB"
)

print("=" * 60)
