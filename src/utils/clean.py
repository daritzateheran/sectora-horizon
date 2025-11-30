import pandas as pd
import unicodedata
import re

def clean_text(value: str):
    if pd.isna(value):
        return None
    text = str(value).strip().upper()
    text = "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    ).strip()
    invalid_tokens = {
        "", "?", "??", "???", ".", "..", "...",
        "NA", "N/A", "NONE", "NULL",
        "SIN NOMBRE", "SIN NOMBRE.",
        "NO APLICA", "NO REGISTRA",
        "S/N", "S/D", "#NOMBRE?", "NAN"
    }
    if text in invalid_tokens: return None
    if is_numeric_string(text): return None
    if not re.search(r"[A-Z0-9]", text): return None
    if re.search(r"[A-Z]", text): return text
    return None

def is_numeric_string(s: str) -> bool: 
    return s.replace(" ", "").isdigit()

def normalize_numeric_code(value: str, digits: int):
    """
    Normaliza códigos numéricos provenientes de texto/float:
    - '1000.0' → '1000'
    - '20.0'   → '20'
    - '0020'   → '0020'
    Devuelve None si no cumple el patrón o los dígitos requeridos.
    """

    if value is None:
        return None
    value = str(value).strip()
    if value == "":
        return None
    if re.match(r"^\d+\.0$", value):
        value = value.split(".")[0]
    if not re.match(r"^\d+$", value):
        return None
    if len(value) != digits:
        return None

    return value


def normalize_code_to_length(value, target_length: int):
    if value is None:
        return None

    text = str(value).strip()

    if re.match(r"^\d+\.0$", text):
        text = text[:-2]
    if not text.isdigit():
        return None
    if len(text) > target_length:
        return None
    return text.zfill(target_length)

def normalize_text(s: str):
    if pd.isna(s):
        return None
    s = str(s).upper().strip()
    s = "".join(
        c for c in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(c)
    )
    s = s.replace(",", "").replace(".", "").strip()
    return s

def to_float(x):
    if pd.isna(x):
        return None
    s = str(x).strip().replace(".", "").replace(",", ".")
    try: return float(s)
    except: return None