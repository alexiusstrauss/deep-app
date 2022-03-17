import requests
from requests.structures import CaseInsensitiveDict
import psycopg2
from decimal import Decimal, getcontext


class MZTools:
    def __init__(
        self,
        found_id: str,
        found_doc: str,
        start_date: str,
        end_date: str,
        token: str,
        resume_file: str,
    ):
        self.found_id = found_id
        self.found_doc = found_doc
        self.start_date = start_date
        self.end_date = end_date
        self.token = token
        self.resume_file = resume_file
        self.url = f"https://api.mziq.com/mzfundsmng/funds/{self.found_id}/reports/profitability?startDate={self.start_date}&endDate={self.end_date}&calculated=true&ignoreFields=value12M,value24M,value36M,value48M,day,month,year,fromStart"

    def get_acumulado_mzqi(self):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(self.url, headers=headers).json()
        if response["series"]:
            value = "{:0.5f}".format(response["series"][0]["data"][-1])
            return float(value)

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
            WHERE fund_doc='{self.found_doc}' and competency_date 
            BETWEEN '{self.start_date}' and '{self.end_date}';
        """
        cursor.execute(query)
        row = cursor.fetchall()

        if not row:
            return None

        return self.convert(
            row[LAST_VALUE][SHARE_VALUE],
            row[FIRST_VALUE][SHARE_VALUE],
        )

    def convert(self, last_value: float, first_value: float) -> float:
        value = "{:0.5f}".format(((last_value / first_value) - 1) * 100)
        return float(value)

    def compare_data(self):
        # Pegar os dados da mzqi e comprar com o cvm no open data
        return self.get_acumulado_mzqi() == self.get_acumulado_cvm()


token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MjJmNWY2ZjQyMmUzYTAwMjNjZGQyOTIiLCJpc3MiOiJNWiBHcm91cCIsImV4cCI6MTY0NzY1NjQyMCwiaWF0IjoxNjQ3NDgzNjIwLCJhdWQiOiJNWiBDb3JlIiwibmFtZSI6IkFsZXhpdXMgTWFycXVlcyIsImVtYWlsIjoiYWxleGl1cy5tYXJxdWVzQG16Z3JvdXAuY29tIiwicmtleSI6ImNvcmU6dXNlcjo2MjJmNWY2ZjQyMmUzYTAwMjNjZGQyOTI6ZGV2aWNlOmVhM2ZkZTE2YWRiYjIxYzc5NmRjOWFlN2UzZjI4MmZjOjY5NDU5MTZkNmVjOTdiN2Y5NjQxNmY1ODJmODI0ZGNkZWZkNWZjMjhmOWMxNGJlNjBlOGM3MjI0MjNkZmQ2NjIiLCJsZWdhY3lVc2VySWQiOiJlYWVjOWQ0NC1lMTFiLTQyNGItYTYzZi1jOTc3ZjE0N2Q4MDQiLCJkZXZpY2VJZCI6ImVhM2ZkZTE2YWRiYjIxYzc5NmRjOWFlN2UzZjI4MmZjIiwiY3VzdG9tZXIiOnsiaWQiOiI1ZjVhNDJiNDI4M2RmOTAxYWUxN2VmNTUiLCJ2YWx1ZSI6IkFSWCBJbnZlc3RpbWVudG9zIiwiZGlzcGxheU5hbWUiOiJBUlggSW52ZXN0aW1lbnRvcyIsImxlZ2FjeUNvbXBhbnlJZCI6ImM4N2ZkNmQxLTc0MTctNDk0Mi05MWJjLWQ5OTUwNjUwYjlmNyIsImxlZ2FjeUlkIjoiYzg3ZmQ2ZDEtNzQxNy00OTQyLTkxYmMtZDk5NTA2NTBiOWY3In19.AIrU1gxmFuetHU56kuzTBVB5ybr7sE0mmyPjIHYfGvQ-rgTC3EZVr7KPClWBQL5Sp3DsEiuyQUxFyeZcESLLKw"
found_id = "60b03acdfd66c40018bfecce"
found_doc = "31353579000108"
start_date = "2020-01-13"
end_date = "2022-01-31"
file_name = "compare.txt"
