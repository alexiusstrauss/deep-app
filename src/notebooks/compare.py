import requests
from requests.structures import CaseInsensitiveDict
import psycopg2
from decimal import Decimal, getcontext


class MZTools:
    START_DATA = "2018-12-01"

    def __init__(
        self,
        fund_id: str,
        fund_doc: str,
        start_date: str,
        end_date: str,
        token: str,
    ):
        self.fund_id = fund_id
        self.fund_doc = fund_doc
        self.start_date = start_date
        self.end_date = end_date
        self.token = token
        self.url = f"https://api.mziq.com/mzfundsmng/funds/{self.fund_id}/reports/profitability?startDate={self.start_date}&endDate={self.end_date}&calculated=true&ignoreFields=value12M,value24M,value36M,value48M,day,month,year,fromStart"

    def get_acumulado_mzqi(self):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(self.url, headers=headers).json()

        return (
            float("{:0.5f}".format(response["series"][0]["data"][-1]))
            if response["series"]
            else float(0)
        )

    def get_acumulado_cvm(self) -> float:
        FIRST_VALUE = 0
        LAST_VALUE = -1
        SHARE_VALUE = 2
        con = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres",
            port=54325,
        )
        cursor = con.cursor()

        query = f"""
            SELECT fund_doc, competency_date, share_value
            FROM cvm_ckan.fi_inf_diario 
            WHERE fund_doc='{self.fund_doc}' and competency_date 
            BETWEEN '{self.start_date}' and '{self.end_date}';
        """
        cursor.execute(query)
        row = cursor.fetchall()

        if not row:
            return float(0)

        return self.convert(
            row[LAST_VALUE][SHARE_VALUE],
            row[FIRST_VALUE][SHARE_VALUE],
        )

    def convert(self, last_value: float, first_value: float) -> float:
        value = "{:0.5f}".format(((last_value / first_value) - 1) * 100)
        return float(value)

    def compare_data(self, intervals: list = None):
        if intervals is None:
            return self.get_acumulado_mzqi() == self.get_acumulado_cvm()
