from typing import List


class StorageInterface:
    """
    Interface for implementing storage services
    """

    class Meta:
        abastract = True

    def list_buckets(self):
        raise NotImplementedError

    def save_to_storage(
        self,
        bucket_name: str,
        data: bytes,
        file_path: str,
        content_type: str,
    ):
        raise NotImplementedError

    def get_or_create_bucket(self, bucket_name: str):
        raise NotImplementedError

    def get_file(self, bucket_name: str, file_path: str):
        raise NotImplementedError

    def delete_file(self, bucket_name: str, file_path: str):
        raise NotImplementedError

    def set_public_access_control(self, bucket_name: str, members: List[str] = None):
        raise NotImplementedError
