# ============================================================
# TEMPLATE REUTILIZÁVEL
# Conversão de Imagens (OneLake / ABFS) → Base64 para Power BI
# Ambiente: Microsoft Fabric / Spark
# Autor: Seu Nome
# ============================================================

# =========================
# CONFIGURAÇÕES
# =========================

# Caminho ABFS da pasta de imagens no OneLake
ABFS_PATH = "abfss://SEU_WORKSPACE_ID@onelake.dfs.fabric.microsoft.com/SEU_LAKEHOUSE_ID/Files/Images"

# Tamanho máximo da imagem (mantém proporção)
# Exemplo: 300 (mais leve), 500 (equilíbrio), 800 (mais qualidade)
IMAGE_MAX_SIZE = 500  

# Qualidade do JPEG (1 a 100)
# Quanto menor, menor o tamanho do arquivo
JPEG_QUALITY = 50  

# Tamanho máximo por linha (limite seguro Power BI)
# Recomendo entre 6000 e 7000
POWERBI_BLOCK_SIZE = 7000  

# =========================
# IMPORTS
# =========================

from pyspark.sql.functions import col, concat, lit, when, posexplode, regexp_extract, substring
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql import functions as F

from PIL import Image
import io
import base64

# =========================
# 1) LEITURA DOS ARQUIVOS BINÁRIOS
# =========================

df_binario = spark.read.format("binaryFile") \
    .option("recursiveFileLookup", "true") \
    .load(ABFS_PATH)

# Filtra apenas imagens válidas
df_binario = df_binario.filter(
    col("path").endswith(".png") |
    col("path").endswith(".jpg") |
    col("path").endswith(".jpeg")
)

# =========================
# 2) CONVERSÃO PARA BASE64 COM REDIMENSIONAMENTO
# =========================

def bytes_para_base64_redimensionado(b):
    if b is None:
        return None

    try:
        imagem = Image.open(io.BytesIO(b))

        # Mantém proporção e reduz tamanho
        imagem.thumbnail((IMAGE_MAX_SIZE, IMAGE_MAX_SIZE))

        # Converte para RGB (remove transparência)
        if imagem.mode in ("RGBA", "P"):
            imagem = imagem.convert("RGB")

        buffer = io.BytesIO()
        imagem.save(
            buffer,
            format="JPEG",
            quality=JPEG_QUALITY,
            optimize=True
        )

        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    except:
        return None


udf_base64 = F.udf(bytes_para_base64_redimensionado, StringType())

df_base64 = df_binario.withColumn(
    "base64",
    udf_base64(col("content"))
)

# =========================
# 3) PREFIXO MIME (Power BI)
# =========================

df_base64 = df_base64.withColumn(
    "base64_com_prefixo",
    concat(lit("data:image/jpeg;base64,"), col("base64"))
)

# =========================
# 4) IDENTIFICAÇÃO DO ARQUIVO
# =========================

df_base64 = df_base64.withColumn(
    "identificacao",
    regexp_extract(col("path"), r"/([^/]+)\.[^.]+$", 1)
)


# =========================
# 5) DIVISÃO EM BLOCOS (LIMITE POWER BI)
# =========================

def split_text(text):
    if text is None:
        return []
    return [text[i:i+POWERBI_BLOCK_SIZE] for i in range(0, len(text), POWERBI_BLOCK_SIZE)]

udf_split = F.udf(split_text, ArrayType(StringType()))

df_split = df_base64.withColumn(
    "blocos",
    udf_split(col("base64_com_prefixo"))
)

# =========================
# 6) EXPLODE PRESERVANDO ORDEM
# =========================

df_exploded = df_split.select(
    "identificacao",
    posexplode(col("blocos")).alias("indice_zero_based", "foto")
)

df_final = df_exploded.withColumn(
    "indice",
    col("indice_zero_based") + 1
).drop("indice_zero_based")


# Camada extra de segurança
df_final = df_final.withColumn(
    "foto",
    substring(col("foto"), 1, POWERBI_BLOCK_SIZE)
)


# =========================
# 7) RESULTADO FINAL
# =========================

display(df_final)

# =========================
# SALVAR TABELA (REUTILIZÁVEL)
# =========================
# Basta alterar abaixo o nome do Lakehouse e o nome desejado para a tabela.

LAKEHOUSE_NAME = "LKH_TESTE"      # <-- Substitua pelo nome do seu Lakehouse
TABLE_NAME = "_gold_fat_fotos"    # <-- Substitua pelo nome desejado da tabela

df_final.write \
    .mode("overwrite") \
    .saveAsTable(f"{LAKEHOUSE_NAME}.{TABLE_NAME}")