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

    def get_data_mzqi(self, token: str):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers = {
            "Authorization": "Bearer " + self.token,
        }
        response = requests.get(self.url, headers=headers)
        return response.json()
    
    def get_data_opendata(self):
        return []
    
    # def compare(self):
    #     data_mzqi = self.get_data_mzqi(self.token)
    #     data_opendata = self.get_data_opendata()
    #     with open(self.to_file, "w") as f:
    #         f.write("date,mzqi,opendata,formula\n")
    #         for i in range(len(data_mzqi["data"])):
    #             f.write(
    #                 f"{data_mzqi['data'][i]['date']},{data_mzqi['data'][i]['value']},{data_opendata[i]['value']},{self.formula(data_mzqi['data'][i]['value'], data_opendata[i]['value'])}\n"
    #             )

    def formula(self, value1, value2):
        return (value2/value1) -1 * 100

found_id = "60b03acdfd66c40018bfecce"
start_date = "2022-01-01"
end_date = "2022-03-01"
file_name = "compare.txt"

mz = MZCompare(found_id, start_date, end_date, bearer_token, file_name)
