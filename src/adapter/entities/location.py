import pandas as pd
from rapidfuzz import process, fuzz
from utils.clean import clean_text, is_numeric_string, normalize_code_to_length, normalize_text

DEPT_CORRECTIONS = {
    "VALLE": "VALLE DEL CAUCA",     
    "GUAJIRA": "LA GUAJIRA",
    "MONTERIA": "CORDOBA",
    "VALLEDUPAR": "CESAR",
    "ARMENIA": "QUINDIO",
}

class Location:
    def __init__(self):
        self

    correct = {
        # Bogotá - Cundinamarca
        "BOGOTA D.C.": "Bogotá - Cundinamarca",
        "CUNDINAMARCA": "Bogotá - Cundinamarca",

        # Centro - Oriente
        "BOYACA": "Centro - Oriente",
        "TOLIMA": "Centro - Oriente",
        "HUILA": "Centro - Oriente",
        "SANTANDER": "Centro - Oriente",
        "NORTE DE SANTANDER": "Centro - Oriente",

        # Costa Atlántica
        "ATLANTICO": "Costa Atlántica",
        "MAGDALENA": "Costa Atlántica",
        "BOLIVAR": "Costa Atlántica",
        "SUCRE": "Costa Atlántica",
        "CORDOBA": "Costa Atlántica",
        "LA GUAJIRA": "Costa Atlántica",
        "CESAR": "Costa Atlántica",

        # Costa Pacífica
        "VALLE DEL CAUCA": "Costa Pacífica",
        "CAUCA": "Costa Pacífica",
        "NARINO": "Costa Pacífica",
        "CHOCO": "Costa Pacífica",

        # ANTIOQUIA
        "ANTIOQUIA": "Antioquia",

        # Eje Cafetero
        "CALDAS": "Eje Cafetero",
        "RISARALDA": "Eje Cafetero",
        "QUINDIO": "Eje Cafetero",

        # Otros (Amazonía – Orinoquía)
        "SAN ANDRES Y PROVIDENCIA": "Otros",
        "META": "Otros",
        "CASANARE": "Otros",
        "ARAUCA": "Otros",
        "GUAVIARE": "Otros",
        "GUAINIA": "Otros",
        "VAUPES": "Otros",
        "VICHADA": "Otros",
        "AMAZONAS": "Otros",
        "CAQUETA": "Otros",
        "PUTUMAYO": "Otros",
    }

    region_oficial = {
        "Andina": [
            "BOGOTA D.C.",
            "ANTIOQUIA",
            "BOYACA",
            "CALDAS",
            "CUNDINAMARCA",
            "HUILA",
            "NORTE DE SANTANDER",
            "QUINDIO",
            "RISARALDA",
            "SANTANDER",
            "TOLIMA",
        ],

        "Caribe": [
            "ATLANTICO",
            "BOLIVAR",
            "CESAR",
            "CORDOBA",
            "LA GUAJIRA",
            "MAGDALENA",
            "SUCRE",
        ],

        "Pacifico": [
            "CAUCA",
            "CHOCO",
            "NARINO",
            "VALLE DEL CAUCA",
        ],

        "Orinoquia": [
            "ARAUCA",
            "CASANARE",
            "META",
            "VICHADA",
        ],

        "Amazonia": [
            "AMAZONAS",
            "CAQUETA",
            "GUAINIA",
            "GUAVIARE",
            "PUTUMAYO",
            "VAUPES",
        ],

        "Insular": [
            "SAN ANDRES Y PROVIDENCIA"
        ],
    }

    @staticmethod
    def normalize_department(s):
        if pd.isna(s):
            return None
        s_clean = clean_text(s)
        return DEPT_CORRECTIONS.get(s_clean, s_clean)
    

    def dept_mapper(self, main_dpts, div_dpts, dept_map):
        for dpto in main_dpts:
            match, score, _ = process.extractOne(
                dpto,
                div_dpts,
                scorer=fuzz.token_sort_ratio
            )
            dept_map[dpto] = match
        return dept_map