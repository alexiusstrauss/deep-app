import requests
from requests.structures import CaseInsensitiveDict


class MzTools:
    def __init__(
        self,
        found_id: str,
        date_in: str,
        date_fin: str,
        token: str,
        resume_file: str,
    ):
        self.found_id = found_id
        self.date_in = date_in
        self.date_fin = date_fin
        self.token = token
        self.resume_file = resume_file
        self.url = f"https://api.mziq.com/mzfundsmng/funds/{self.found_id}/reports/profitability?startDate={self.date_in}&endDate={self.date_fin}&calculated=true&ignoreFields=value12M,value24M,value36M,value48M,day,month,year,fromStart"

    def get_data_mzqi(self, token: str):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(self.url, headers=headers)
        return response.json()
    
    def get_data_opendata(self):
        return []
    
    @staticmethod
    def get_last_revision_imported():
        conn = pg_hook.get_conn()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = """
            SELECT
                *
            FROM
                cvm_ckan.fi_cad
            ORDER BY ckan_timestamp desc
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()

        if not row:
            return None
        
        return row
        

    def formula(self, value1, value2):
        return (value2/value1) -1 * 100

found_id = "60b03acdfd66c40018bfecce"
start_date = "2022-01-01"
end_date = "2022-03-01"
file_name = "compare.txt"

