from service.etl import ETL
from adapter.entities.company import CompanyEDA
from ingest.catalog import DatasetCatalog
from ingest.loader import RawDatasetLoader
from ingest.fetch.csv import CsvAdapter
from ingest.fetch.sct import SocrataAdapter
from ingest.fetch.excel import ExcelAdapter
from adapter.entities.ciiu import Ciiu
from adapter.entities.location import Location
from adapter.entities.year import ReportYear
from adapter.entities.macroeco import MacroEco
from sqlalchemy import create_engine
import pandas as pd
from envt.config import load_config
import traceback
from helper.logging.logger import Logger

log = Logger("file_register", log_to_file=False, level="INFO")


def main():

    log.info('Initiating ETL Service...')

    try:
        config_load = load_config()

        engine = create_engine(
        f'postgresql://{config_load.user}:{config_load.password}@{config_load.host}:{config_load.port}/{config_load.db}'
        )
    

        eda = ETL(
            config=config_load,
            engine=engine,
            company=CompanyEDA(),
            ciiu=Ciiu(),
            location = Location(),
            year=ReportYear(),
            macroeco=MacroEco(),
            catalog=DatasetCatalog(),
            loader = RawDatasetLoader(
            csv_adapter=CsvAdapter(),
            sct_adapter=SocrataAdapter(),
            excel_adapter=ExcelAdapter(),
            ),
        )

        df_company, df_ciiu, df_loc, df_year, df_macroeco = eda.eda_build(name="empresas_10k")

        tables = {
            'Company': df_company,
            'Ciiu': df_ciiu,
            'Location': df_loc,
            'ReportYear': df_year,
            'MacroEconomy': df_macroeco
            # 'FinancialDerived': df_
        }
        for n in tables:
            load = eda.load(tables[n], n)   

        log.info('Migration completed succesfully!')

    except Exception as e:
        log.error(f'Process failed wit error: {e}')
        traceback.print_exc()

if __name__ == "__main__":
    main()
