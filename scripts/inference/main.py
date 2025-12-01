import pandas as pd
import os
import joblib
import lightgbm as lgb

CHECKPOINT_DIR = "/workspaces/data-ecosystem/models/"

print("Cargando modelos...")

modelo_servicios = lgb.Booster(model_file=os.path.join(CHECKPOINT_DIR, "modelo_servicios.txt"))
modelo_general   = lgb.Booster(model_file=os.path.join(CHECKPOINT_DIR, "modelo_general.txt"))
features = joblib.load(os.path.join(CHECKPOINT_DIR, "features.pkl"))

print("Modelos cargados")
print(f"{len(features)} features cargadas")

def run_inference(csv_path, output_path, year_to_predict=2025, pib=3.0, dtf=8.0):
    print(f"\nProcesando CSV: {csv_path}")
    df = pd.read_csv(csv_path)

    df = df.sort_values("year").groupby("nit").tail(1).copy()
    df["PIB_Crecimiento"] = pib
    df["Tasa_Interes_DTF"] = dtf
    sector_cols = [c for c in df.columns if c.startswith("sector_")]
    for col in sector_cols:
        df[f"{col}_x_PIB"] = df[col] * df["PIB_Crecimiento"]
        df[f"{col}_x_DTF"] = df[col] * df["Tasa_Interes_DTF"]

    df["Prediccion_Margen"] = 0.0

    mask_serv = df["sector_SERVICIOS"] == 1
    df_serv = df[mask_serv]
    df_rest = df[~mask_serv]

    if not df_serv.empty:
        pred_serv = modelo_servicios.predict(df_serv[features])
        df.loc[mask_serv, "Prediccion_Margen"] = pred_serv

    if not df_rest.empty:
        pred_gen = modelo_general.predict(df_rest[features])
        df.loc[~mask_serv, "Prediccion_Margen"] = pred_gen

    df["Ganancia_Proyectada_Mils"] = df["Prediccion_Margen"] * df["ingresos"]

    cols_export = [
        "nit","razon_social","macrosector_calc","region_calc",
        "ingresos","ganancias",
        "Prediccion_Margen","Ganancia_Proyectada_Mils"
    ]

    df[cols_export].to_csv(output_path, index=False)
    print(f"archivo exportado a: {output_path}")

    return df[cols_export]


if __name__ == "__main__":
    INPUT = "/workspaces/data-ecosystem/data/processed/master_empresas_enriched.csv"
    OUTPUT = "/workspaces/data-ecosystem/data/processed/predicciones_2025.csv"
    run_inference(INPUT, OUTPUT)
