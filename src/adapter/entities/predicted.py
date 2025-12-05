import pandas as pd
from utils.clean import clean_text
from utils.uuid import generate_deterministic_id_name_based

class PredictionEDA:
    """
    Procesa el dataset 'predicted' proveniente del modelo.
    Normaliza, asigna company_id, y prepara columnas para ReportYearPrediction.
    """

    def __init__(self):
        self

    def clean_predicted(self, df):
        """
        Normaliza columnas básicas del CSV:
        nit, razon_social, macrosector_calc, region_calc, ingresos, ganancias, 
        Prediccion_Margen, Ganancia_Proyectada_Mils
        """
        
        df["razon_social"] = df["razon_social"].apply(clean_text)
        df["nit"] = df["nit"].astype(str).str.strip()
        df["company_id"] = df["razon_social"].apply(generate_deterministic_id_name_based)
        df = df.rename(columns={
            "Prediccion_Margen": "prediccion_margen",
            "Ganancia_Proyectada_Mils": "ganancia_proyectada",
            "region_calc": "region_natural" 
        })
        return df
