import requests
from requests.structures import CaseInsensitiveDict
import psycopg2


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

    def get_data_mzqi(self, token: str):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers = {
            "Authorization": "Bearer " + self.token,
        }
        response = requests.get(self.url, headers=headers)
        return response.json()
    
    def get_data_opendata(self):
        con = psycopg2.connect(host='localhost', database='postgres',
        user='postgres', password='postgres', port=54325)
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
        
        return row
        

    def formula(self, value1, value2):
        return (value2/value1) -1 * 100
    
    def compare_data(self):
        # Pegar os dados da mzqi e comprar com o opendataDB
        return True


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFsZXhpdXMubWFycXVlc0Btemdyb3VwLmNvbSIsImJlYXJlcl90b2tlbl9pc3N1ZWRfYXQiOjE2NDc0NDk2ODIxMDUsImJlYXJlcl90b2tlbl9leHBpcmVzX2F0IjoiMjAyMi0wMy0xOFQxNjo1NDo0Mi4xMDVaIiwiaWF0IjoxNjQ3NDQ5NjgyfQ.4CvRwUYtPxmt1OQS6oyaTP9DElhvdPpIswv-6hGsi1M"
found_id = "60b03acdfd66c40018bfecce"
found_doc = "03168062000103"
start_date = "2022-01-01"
end_date = "2022-03-01"
file_name = "compare.txt"

