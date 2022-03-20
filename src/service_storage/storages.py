import os
from typing import List

from google.cloud import storage
from service_storage.interfaces import StorageInterface


class GoogleStorage(StorageInterface):
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_storage/credentials.json"

    def list_buckets(self) -> dict:
        """
        Lists all buckets
        """
        storage_client = storage.Client()
        buckets = storage_client.list_buckets()
        return {bucket.name: bucket for bucket in buckets}


    def save_to_storage(
        self,
        bucket_name: str,
        data: bytes,
        file_path: str,
        content_type: str = "application/pdf",
    ):
        """
        Saves a file to Google Cloud Storage
        default content type is application/pdf
        Return: public url
        """
        bucket = self.get_or_create_bucket(bucket_name)
        blob = bucket.blob(file_path)
        try:
            blob.upload_from_string(data, content_type=content_type)
            return blob
        except Exception as error:
            print(error)
            return None

    def get_or_create_bucket(self, bucket_name: str):
        client_storage = storage.Client()

        if storage.Bucket(client_storage, bucket_name.lower()).exists():
            return client_storage.get_bucket(bucket_name.lower())
        else:
            return client_storage.create_bucket(bucket_name.lower())

    def delete_file(self, bucket_name: str, file_path: str):
        blob = self.get_file(bucket_name, file_path)
        return blob.delete() if blob else False

    def get_file(self, bucket_name: str, file_path: str):
        bucket = self.get_or_create_bucket(bucket_name)
        blob = bucket.blob(file_path)
        return blob if blob.exists() else None

    def set_public_access_control(self, bucket_name: str, members: List[str] = None):
        if members is None:
            members = ["allUsers"]
        bucket = self.get_or_create_bucket(bucket_name)

        policy = bucket.get_iam_policy(requested_policy_version=3)
        policy.bindings.append(
            {"role": "roles/storage.objectViewer", "members": members}
        )

        bucket.set_iam_policy(policy)
        print(f"Bucket {bucket.name} definido como publico")
