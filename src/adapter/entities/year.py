import pandas as pd


class ReportYear:
    def __init__(self):
        self,

        self.financial_cols = [
            "ingresos_operacionales",
            "ganancia_p_rdida",
            "total_activos",
            "total_pasivos",
            "total_patrimonio"
        ]
    
    def fix_data(self, df):

        for c in self.financial_cols:
            df[c] = df[c].astype(str)\
                        .str.replace("$", "", regex=False)\
                        .str.replace(".", "", regex=False)\
                        .str.replace(",", ".", regex=False)\
                        .astype(float) 
            df[c] = pd.to_numeric(df[c], errors='coerce')
        return df