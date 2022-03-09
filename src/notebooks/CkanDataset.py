

class CKANDataSet:
    
    def init(self, url: str, file_name: str, temp_dir: str = "tmp"):
        self.url = url
        self.file_name = file_name
        self.temp_dir = temp_dir
        self.df = None
        
    def download(self):
        pass
    
    def __format_doc(self, value):
        pass
    
    def delete_local_file(self, file_path: str):
        pass
    
    def open_file(self, file: str):
        pass
    
    def process_file(self):
        pass
    
    def __create_engine(self, config: dict):
        pass
    
    def save_to_db(self):
        pass
    
    
        