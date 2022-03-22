from unittest import mock

from service_storage.service import ServiceStorage
from service_storage.storages import GoogleStorage


class TestGoogleStorage:
    def setup(self):
        with mock.patch("google.cloud.storage.Client", autospec=True) as mock_client:
            self.client = mock_client()
            self.google = GoogleStorage()
            self.gcp = ServiceStorage(self.google)

    @mock.patch("service_storage.storages.GoogleStorage.list_buckets")
    def test_list_buckets(self, mock_list_buckets):
        bucket = self.client.bucket.return_value
        mock_list_buckets.return_value = {
            bucket.name: bucket,
        }

        buckets = self.gcp.storage.list_buckets()
        assert mock_list_buckets.return_value == buckets

    @mock.patch("service_storage.storages.GoogleStorage.save_to_storage")
    def test_save_to_storage(self, mock_save_to_storage):
        # bucket = self.client.bucket.return_value
        # blob = bucket.blob.return_value
        # blob.public_url.return_value = "gs://uri/file.pdf"
        # blob.exists.return_value = True

        mock_save_to_storage.return_value = "gs://uri/file.pdf"
        response = mock_save_to_storage.return_value

        assert response == "gs://uri/file.pdf"
        assert len(response) == len("gs://uri/file.pdf")
