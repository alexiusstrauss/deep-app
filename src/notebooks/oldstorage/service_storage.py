from google.cloud import storage
import os
from typing import List

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_storage/credentials.json"


class ServiceStorage:
    @staticmethod
    def list_buckets():
        """
        Lists all buckets
        """
        storage_client = storage.Client()
        return storage_client.list_buckets()

    @staticmethod
    def save_to_storage(
        bucket_name: str,
        data: bytes = None,
        file_path: str = None,
        content_type: str = "application/pdf",
    ):
        """
        Saves a file to Google Cloud Storage
        default content type is application/pdf
        Return: public url
        """
        bucket = ServiceStorage.get_bucket(bucket_name)
        blob = bucket.blob(file_path)
        try:
            blob.upload_from_string(data, content_type=content_type)
            return blob
        except Exception as error:
            print(error)
            return None

    @staticmethod
    def delete_file(bucket_name: str, file_name: str) -> bool:
        bucket = ServiceStorage.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        if blob.exists():
            blob.delete()
            return True
        else:
            return False

    @staticmethod
    def get_bucket(bucket_name: str) -> storage.Bucket:
        client_storage = storage.Client()

        if storage.Bucket(client_storage, bucket_name.lower()).exists():
            return client_storage.get_bucket(bucket_name.lower())
        else:
            return client_storage.create_bucket(bucket_name.lower())

    @staticmethod
    def set_bucket_public_iam(
        bucket_name: str,
        members: List[str] = None,
    ):

        if members is None:
            members = ["allUsers"]
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        policy = bucket.get_iam_policy(requested_policy_version=3)
        policy.bindings.append(
            {"role": "roles/storage.objectViewer", "members": members}
        )

        bucket.set_iam_policy(policy)
        print(f"Bucket {bucket.name} definido como publico")
