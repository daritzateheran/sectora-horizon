from utils.clean import to_float
import pandas as pd

class MacroEco:
    def __init__(self):
        pass

    def clean(self, df_raw):
        df = df_raw.iloc[1:].reset_index(drop=True)
        df = df[df['Fecha'].astype(str).str.len() == 10].reset_index(drop=True)

        df.columns = [f"col_{i}" for i in range(df.shape[1])]

        # Remove Colcap (col_1)
        if "col_1" in df.columns:
            df.drop(columns=["col_1"], inplace=True)

        df["year"] = df["col_0"].str[-4:].astype(int)

        df_macro = pd.DataFrame({
            "year": df["year"],
            "gdp_nominal": df["col_2"].apply(to_float),
            "gdp_nominal_pct": df["col_3"].apply(to_float),
            "gdp_real": df["col_4"].apply(to_float),
            "gdp_real_pct": df["col_5"].apply(to_float),
            "gdp_nominal_growth": df["col_6"].apply(to_float),
            "gdp_real_growth": df["col_7"].apply(to_float),
            "cpi": df["col_8"].apply(to_float),
            "population": df["col_9"].apply(to_float),
        })

        return df_macro.sort_values("year").reset_index(drop=True)
