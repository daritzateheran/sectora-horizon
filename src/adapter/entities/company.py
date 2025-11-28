from utils.clean import clean_text, is_numeric_string, normalize_code_to_length
import pandas as pd
import numpy as np

class CompanyEDA:
    def __init__(self):
        self

    def choose_base_from_names(self, names: list) -> str:
        """
        - Si hay strings, el base será el string más frecuente.
        - Si todos son numéricos, base = número más frecuente.
        """
        values = list(names)
        numeric = [n for n in values if is_numeric_string(n)]
        stringy = [n for n in values if not is_numeric_string(n)]

        if stringy:
            counts = pd.Series(stringy).value_counts()
            return counts.idxmax()
        counts = pd.Series(numeric).value_counts()
        return counts.idxmax()

    def detect_identity_inconsistencies(self, df, id_col, name_col):
        # ID → nombres
        id_groups = (
            df.groupby(id_col)
            .agg(
                names=(name_col, lambda x: sorted(set(x))),
                n_names=(name_col, "nunique")
            )
            .reset_index()
        )
        inconsistent_id = id_groups[id_groups["n_names"] > 1]
        # Nombre → IDs
        name_groups = (
            df.groupby(name_col)
            .agg(
                ids=(id_col, lambda x: sorted(set(x))),
                n_ids=(id_col, "nunique")
            )
            .reset_index()
        )
        inconsistent_name = name_groups[name_groups["n_ids"] > 1]
        return inconsistent_id, inconsistent_name

    def choose_base_dynamic(self, group, name_col, id_col, year_col):
        if year_col in group.columns:
            max_year = group[year_col].max()
            sub = group[group[year_col] == max_year]
            
            cleaned = [clean_text(n) for n in sub[name_col] if clean_text(n)]
            if cleaned:
                return pd.Series(cleaned).value_counts().idxmax()    
        cleaned_all = [clean_text(n) for n in group[name_col].unique() if clean_text(n)]
        if cleaned_all:
            return pd.Series(cleaned_all).value_counts().idxmax()
        return group[id_col].iloc[0]

    def build_base_names(self, df, id_col, name_col, year_col="a_o_de_corte"):
        base_names = {}
        for nit, group in df.groupby(id_col):
            base = self.choose_base_dynamic(group, name_col, id_col, year_col)
            base_names[nit] = base
        return base_names


    def apply_stage1(self, df, id_col, base_names):
        df["name_stage1"] = df[id_col].map(base_names)
        return df

    def detect_multi_nit_names(self, df, name_col, id_col):
        name_groups = (
            df.groupby(name_col)
            .agg(nits=(id_col, lambda x: sorted(set(x))), n_ids=(id_col, "nunique"))
            .reset_index()
        )
        multi = name_groups[name_groups["n_ids"] > 1]
        return multi

    def apply_stage2(self, df, id_col, name_col, multi):
        multi_names = set(multi[name_col].tolist())
        
        df["canonical_name"] = df.apply(
            lambda row:
                f"{row[name_col]}__{row[id_col]}"
                if row[name_col] in multi_names
                else row[name_col],
            axis=1
        )
        return df