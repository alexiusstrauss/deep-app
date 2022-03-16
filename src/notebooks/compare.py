import requests
from requests.structures import CaseInsensitiveDict


class MZCompare:
    def __init__(
        self,
        found_id: str,
        date_in: str,
        date_fin: str,
        token: str,
        to_file: str,
    ):
        self.found_id = found_id
        self.date_in = date_in
        self.date_fin = date_fin
        self.token = token
        self.to_file = to_file
        self.url = f"https://api.mziq.com/mzfundsmng/funds/{self.found_id}/reports/profitability?startDate={self.date_in}&endDate={self.date_fin}&calculated=true&ignoreFields=value12M,value24M,value36M,value48M,day,month,year,fromStart"

    def get_data(self, token: str):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MjJmNWY2ZjQyMmUzYTAwMjNjZGQyOTIiLCJpc3MiOiJNWiBHcm91cCIsImV4cCI6MTY0NzQ4MDI1MiwiaWF0IjoxNjQ3MzA3NDUyLCJhdWQiOiJNWiBDb3JlIiwibmFtZSI6IkFsZXhpdXMgTWFycXVlcyIsImVtYWlsIjoiYWxleGl1cy5tYXJxdWVzQG16Z3JvdXAuY29tIiwicmtleSI6ImNvcmU6dXNlcjo2MjJmNWY2ZjQyMmUzYTAwMjNjZGQyOTI6ZGV2aWNlOmVhM2ZkZTE2YWRiYjIxYzc5NmRjOWFlN2UzZjI4MmZjOmJlNzM2NGMwMWQ3NTcxZWRiNzBiMzkyOWU4NmMyODU4NTJhMzA3NDk2NGMwNmRiNjE0MWUwZjY2OGU3NDlkZGEiLCJsZWdhY3lVc2VySWQiOiJlYWVjOWQ0NC1lMTFiLTQyNGItYTYzZi1jOTc3ZjE0N2Q4MDQiLCJkZXZpY2VJZCI6ImVhM2ZkZTE2YWRiYjIxYzc5NmRjOWFlN2UzZjI4MmZjIiwiY3VzdG9tZXIiOnsiaWQiOiI1ZjVhNDJiNDI4M2RmOTAxYWUxN2VmNTUiLCJ2YWx1ZSI6IkFSWCBJbnZlc3RpbWVudG9zIiwiZGlzcGxheU5hbWUiOiJBUlggSW52ZXN0aW1lbnRvcyIsImxlZ2FjeUNvbXBhbnlJZCI6ImM4N2ZkNmQxLTc0MTctNDk0Mi05MWJjLWQ5OTUwNjUwYjlmNyIsImxlZ2FjeUlkIjoiYzg3ZmQ2ZDEtNzQxNy00OTQyLTkxYmMtZDk5NTA2NTBiOWY3In19.4RF6RSY4h25MAKTja5D6gak3bAlEoKUz0TMa4oIUVKwPp_L-_rmrO7woCs30JcpDsE5jF-T8vawtoPJIc-Bhkw"
        }
        response = requests.get(self.url, headers=headers)
        return response.json()

    def formula(self, value1, value2):
        return (value2/value1) -1 * 100

bearer_token = """
eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MjJmNWY2ZjQyMmUzYTAwMjNjZGQyOTIiLCJpc3MiOiJNWiBHcm91cCIsImV4cCI6MTY0NzQ4MDI1MiwiaWF0IjoxNjQ3MzA3NDUyLCJhdWQiOiJNWiBDb3JlIiwibmFtZSI6IkFsZXhpdXMgTWFycXVlcyIsImVtYWlsIjoiYWxleGl1cy5tYXJxdWVzQG16Z3JvdXAuY29tIiwicmtleSI6ImNvcmU6dXNlcjo2MjJmNWY2ZjQyMmUzYTAwMjNjZGQyOTI6ZGV2aWNlOmVhM2ZkZTE2YWRiYjIxYzc5NmRjOWFlN2UzZjI4MmZjOmJlNzM2NGMwMWQ3NTcxZWRiNzBiMzkyOWU4NmMyODU4NTJhMzA3NDk2NGMwNmRiNjE0MWUwZjY2OGU3NDlkZGEiLCJsZWdhY3lVc2VySWQiOiJlYWVjOWQ0NC1lMTFiLTQyNGItYTYzZi1jOTc3ZjE0N2Q4MDQiLCJkZXZpY2VJZCI6ImVhM2ZkZTE2YWRiYjIxYzc5NmRjOWFlN2UzZjI4MmZjIiwiY3VzdG9tZXIiOnsiaWQiOiI1ZjVhNDJiNDI4M2RmOTAxYWUxN2VmNTUiLCJ2YWx1ZSI6IkFSWCBJbnZlc3RpbWVudG9zIiwiZGlzcGxheU5hbWUiOiJBUlggSW52ZXN0aW1lbnRvcyIsImxlZ2FjeUNvbXBhbnlJZCI6ImM4N2ZkNmQxLTc0MTctNDk0Mi05MWJjLWQ5OTUwNjUwYjlmNyIsImxlZ2FjeUlkIjoiYzg3ZmQ2ZDEtNzQxNy00OTQyLTkxYmMtZDk5NTA2NTBiOWY3In19.4RF6RSY4h25MAKTja5D6gak3bAlEoKUz0TMa4oIUVKwPp_L-_rmrO7woCs30JcpDsE5jF-T8vawtoPJIc-Bhkw
"""
found_id = "60b03acdfd66c40018bfecce"
start_date = "2022-01-01"
end_date = "2022-03-01"
file_name = "compare.txt"

mz = MZCompare(found_id, start_date, end_date, bearer_token, file_name)
