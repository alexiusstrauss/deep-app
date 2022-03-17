# Imports the Google Cloud client library
import os
from google.cloud import storage


class ServiceStorage:
    """
        Bucket Principa: s4_pdf_bucket/<farm_id>/<user_id>/file_name.pdf
    """    
    
    @staticmethod
    def list_buckets():
        """
        Lists all buckets
        """
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./credentials.json"
        
        storage_client = storage.Client()
        storage_client.bucket()
        return storage_client.list_buckets()
    
    @staticmethod
    def save_to_storage(bucket_name, file_name, file_path):
        """
        Saves a file to Google Cloud Storage
        """
        bucket = ServiceStorage.__get_bucket(bucket_name)

        # Uploads the file
        blob = bucket.blob(file_name)
        blob.upload_from_filename(file_path)
        print("File {} uploaded to {}.".format(file_name, bucket_name))

    def __get_bucket(self, bucket_name):
        """
        Return bucket instance
        """

        bucket = ServiceStorage.__bucket_exists(bucket_name)

        if not bucket:
            bucket = ServiceStorage.__create_bucket(bucket_name)

        return bucket

    def __bucket_exists(self, bucket_name):
        """
        Checks if bucket exists
        """
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        return bucket is not None

    def __create_bucket(self, bucket_name):
        """
        Creates a bucket
        """
        storage_client = storage.Client()
        return storage_client.create_bucket(bucket_name)
