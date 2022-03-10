import os
import re
import requests
import pandas as pd
from sqlalchemy import create_engine


class CKANDataSet:
    def __init__(self, url: str, file_name: str, temp_dir: str = "tmp"):
        self.url = url
        self.file_name = file_name
        self.temp_dir = temp_dir
        self.df = None
        self.response = {}
        self.config = {
            "host": "localhost",
            "database": "postgres",
            "user": "postgres",
            "password": "postgres",
        }

    def download(self):
        temp_file = f"{self.temp_dir}/{self.file_name}"
        response = requests.get(self.url, stream=True)

        if response.status_code == 200:
            with open(temp_file, "wb") as new_file:
                for partial in response.iter_content(chunk_size=256):
                    new_file.write(partial)

            self.response = {
                "file_path": temp_file,
                "file_name": self.file_name,
                "date_ref": re.sub(r"[^0-9]", "", self.url),
            }
        else:
            response.raise_for_status()

    def delete_local_file(self) -> bool:
        """
        Delete local file
        """
        if os.path.exists(self.response.get("file_path")):
            try:
                os.remove(self.response.get("file_path"))
                return True
            except OSError as err:
                raise OSError(err) from err

    def open_file(self):
        self.df = pd.read_csv(
            self.response.get("file_path"),
            sep=";",
            encoding="latin-1",
        )
        pd.set_option("display.precision", 7)

    def process_file(self):
        self.df = self.df.loc[
            (self.df["CNPJ_FUNDO"] == "03.168.062/0001-03")
            | (self.df["CNPJ_FUNDO"] == "10.237.480/0001-62")
            | (self.df["CNPJ_FUNDO"] == "04.515.848/0001-04")
            | (self.df["CNPJ_FUNDO"] == "30.921.203/0001-81")
            | (self.df["CNPJ_FUNDO"] == "30.910.553/0001-42")
            | (self.df["CNPJ_FUNDO"] == "32.102.131/0001-76")
            | (self.df["CNPJ_FUNDO"] == "30.910.199/0001-56")
            | (self.df["CNPJ_FUNDO"] == "37.368.116/0001-98")
            | (self.df["CNPJ_FUNDO"] == "06.041.290/0001-06")
            | (self.df["CNPJ_FUNDO"] == "17.414.721/0001-40")
            | (self.df["CNPJ_FUNDO"] == "35.927.302/0001-94")
            | (self.df["CNPJ_FUNDO"] == "31.353.579/0001-08")
            | (self.df["CNPJ_FUNDO"] == "03.879.361/0001-48")
        ]

        self.df["CNPJ_FUNDO"] = self.df["CNPJ_FUNDO"].apply(self.format_doc)

        # Rename columns
        rename_map = {
            "CNPJ_FUNDO": "fund_doc",
            "DT_COMPTC": "competency_date",
            "VL_TOTAL": "amount",
            "VL_QUOTA": "share_value",
            "VL_PATRIM_LIQ": "equity_value",
            "NR_COTST": "quotaholder_number",
        }

        self.df = self.df.rename(columns=rename_map)

        # Columns to keep
        cols_keep = [
            "fund_doc",
            "competency_date",
            "amount",
            "share_value",
            "equity_value",
            "quotaholder_number",
        ]
        self.df = self.df[cols_keep]

        # add column with the date of the file
        self.df["data_ref"] = self.response.get("date_ref")
        return True

    def format_doc(self, document) -> any:
        """
        Format value for 14 digits
        """
        if pd.isna(document):
            return None
        doc = re.sub(r"[^0-9]", "", document)
        return doc.zfill(14)

    def save_to_db(self):
        engine = self.create_engine(self.config)
        self.df.to_sql(
            "fi_inf_diario",
            con=engine,
            schema="cvm_ckan",
            index=False,
            if_exists="append",
        )

        return True

    def create_engine(self, config: dict):
        connect = "postgresql+psycopg2://%s:%s@%s:54325/%s" % (
            config["user"],
            config["password"],
            config["host"],
            config["database"],
        )
        return create_engine(connect)
