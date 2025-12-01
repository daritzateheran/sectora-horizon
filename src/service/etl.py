from ingest.catalog import DatasetCatalog
from ingest.loader import RawDatasetLoader
from utils.uuid import generate_deterministic_id_name_based
from utils.clean import clean_text, normalize_code_to_length, normalize_text
import pandas as pd
import psutil, os, gc

def mem():
    print(f"Memory: {psutil.Process(os.getpid()).memory_info().rss/1024**2:.1f} MB")

class ETL:
    def __init__(self,
            config,
            engine,
            company,
            ciiu,
            location,
            year,
            macroeco,
            # financial,
            catalog=DatasetCatalog,
            loader=RawDatasetLoader,
    ):
        self.config = config
        self.engine = engine
        self.company = company
        self.ciiu = ciiu
        self.location = location
        self.year = year
        self.macroeco = macroeco
        # self.financial = financial
        self.catalog = catalog
        self.loader = loader

    def eda_build(self, name=str):
        
        df_10k = self._get_fixed_data(name)

        ## Company
        df_company = self._build_company(df_10k)

        ## Ciiu
        df_10k["ciiu_code"] = df_10k["ciiu"].apply(lambda x: normalize_code_to_length(x, 4))
        ciiu = self._get_fixed_data("ciiu")
        df_ciiu = self._fix_ciiu(ciiu)

        ## Location
        df_div = self._get_fixed_data("divipola")
        df_loc = self._fix_dept(df_10k, df_div)

        ## Year
        fix_fina = self._fix_financial(df_10k, df_ciiu, df_loc)

        ## MacroEconomical
        df_banrep_raw = self._get_fixed_data("ban_rep")
        df_macro = self.macroeco.clean(df_banrep_raw)

        return df_company, df_ciiu, df_loc, fix_fina, df_macro
    
    def load(self, df, tbl):
        try:
            rows_imported = 0

            
            print(f'importing rows {rows_imported} to {rows_imported + len(df)} into {tbl}... ')
            
            df.to_sql(tbl, self.engine, if_exists='replace', index=False)
            rows_imported += len(df)

            print("Data imported successful")

        except Exception as e:

            print("Data load error: " + str(e))
    
    # ---------------- Internals ----------------

    def _get_fixed_data(self, name: str) -> pd.DataFrame:
        ds = self.catalog.get(name)
        records = list(self.loader.load(ds))
        return pd.DataFrame(records)
    
    def _build_company(self, df):
        df.raz_n_social = df.apply(
            lambda row: clean_text(row.raz_n_social) or row.nit, axis=1
        )

        base_names = self.company.build_base_names(df, "nit", "raz_n_social")
        df = self.company.apply_stage1(df, "nit", base_names)

        multi = self.company.detect_multi_nit_names(df, "name_stage1", "nit")
        df = self.company.apply_stage2(df, "nit", "name_stage1", multi)

        df.drop(columns=["name_stage1", "raz_n_social"], inplace=True)

        df.rename(columns={"canonical_name": "raz_n_social"}, inplace=True)

        df["company_id"] = df["raz_n_social"].apply(generate_deterministic_id_name_based)

        return df[["company_id", "nit", "raz_n_social"]]
    
    def _fix_ciiu(self, df):
        
        ciiu_valid_set = set(
            df["ciiu_code"]
                .dropna()
                .astype(str)
                .unique()
        )
        
        df["ciiu_code"] = df["ciiu_code"].apply(
        lambda x: self.ciiu.impute_missing_ciiu(x, ciiu_valid_set)
        )

        df['div/grp']= df[['division_code', 'group_code']].astype(str).agg('/'.join, axis=1)

        get_group_from_id = lambda id_value: next((name for start, end, name in self.ciiu.ranges if start <= id_value <= end), None)
        df['macrosector_calc'] = (df['ciiu_code'].astype(int)).apply(get_group_from_id)
        return df[["ciiu_code", "div/grp", "division_desc", "macrosector_calc"]]

    def _fix_dept(self, main_df, dept_df):

        main_df.departamento_domicilio = main_df.apply(
        lambda row: clean_text(row.departamento_domicilio), axis=1
        )

        main_df["departamento_domicilio"] = main_df["departamento_domicilio"].apply(self.location.normalize_department)

        main_df["regi_n_corregida"] = main_df["departamento_domicilio"].map(self.location.correct)

        dept_to_region = {
            dept: region
            for region, dept_list in self.location.region_oficial.items()
            for dept in dept_list
        }

        main_df["region_oficial"] = main_df["departamento_domicilio"].map(dept_to_region)

        dept_df["nom_mpio_clean"] = dept_df["nom_mpio"].apply(normalize_text)
        dept_df["dpto_clean"]     = dept_df["dpto"].apply(normalize_text)

        unique_10k_dptos = main_df.departamento_domicilio.dropna().unique()
        unique_div_dptos = dept_df.dpto_clean.dropna().unique()

        dept_map = {}

        dept_map = self.location.dept_mapper(unique_10k_dptos, unique_div_dptos, dept_map)

        main_df.departamento_domicilio = main_df.departamento_domicilio.map(dept_map)

        dept_to_code = (
            dept_df.drop_duplicates(subset=["dpto_clean"])[["dpto_clean", "cod_dpto"]]
            .set_index("dpto_clean")["cod_dpto"]
            .to_dict()
        )

        main_df["departamento_code"] = main_df["departamento_domicilio"].map(dept_to_code)

        main_df["departamento_code"] = main_df["departamento_domicilio"].map(dept_to_code)

        df_dept = (
            dept_df[["cod_dpto", "dpto", "dpto_clean"]]
            .drop_duplicates("cod_dpto")
            .rename(columns={
                "cod_dpto": "departamento_code",
                "dpto": "departamento_name"
            })
        )

        main_df = main_df.merge(
        df_dept[["departamento_code", "departamento_name"]],
        on="departamento_code",
        how="left"
        )

        main_df = (
            main_df[["departamento_code", "departamento_name", "regi_n_corregida", "region_oficial"]]
            .rename(columns={
                "departamento_code": "dept_code",
                "departamento_name": "dept_name",
                "regi_n_corregida": "region_raw",
                "region_oficial": "region_natural",
            })
        )

        return main_df[["dept_code", "dept_name", "region_raw", "region_natural"]]
    
    def _fix_financial(self, main_df, ciiu, loc):

        main_df = self.year.fix_data(main_df)

        main_df.rename(columns={
            "a_o_de_corte": "year",
            "ingresos_operacionales": "ingresos",
            "ganancia_p_rdida": "ganancias",
            "total_activos": "activos",
            "total_pasivos": "pasivos",
            "total_patrimonio": "patrimonio",
        }, inplace=True)

        main_df = main_df.merge(
            ciiu[["ciiu_code", "macrosector_calc"]],
            on="ciiu_code",
            how="left",
            copy=False
        )


        main_df.rename(columns={"departamento_code":"dept_code"}, inplace=True)

        main_df['dept_name']=loc['dept_name']

        return main_df[["company_id", "year", "ciiu_code", "macrosector_calc", "dept_code", "dept_name", "ingresos", "ganancias", "activos", "pasivos", "patrimonio", "supervisor"]]