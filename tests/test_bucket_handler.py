import unittest
from unittest.mock import patch, MagicMock

import bucket_handler
from bucket_handler import BucketHandler


class FakeSession:
    def __init__(self):
        self.client = MagicMock()


class FakeBoto3:
    def __init__(self):
        self._session = FakeSession()
        self.session = self

    def Session(self):
        return self._session


class TestBucketHandler(unittest.TestCase):
    def test_init(self):
        bucket_handler.boto3 = fake_boto3 = FakeBoto3()
        bh = BucketHandler(
            'aws_access_key_id',
            'aws_secret_access_key',
            'bucket_type',
            'specific_storage_name',
        )
        fake_boto3._session.client.assert_called_once_with(
            service_name='s3',
            endpoint_url='https://hb.bizmrg.com',
            aws_access_key_id='aws_access_key_id',
            aws_secret_access_key='aws_secret_access_key',
        )
        self.assertEqual(bh.specific_storage_name, 'specific_storage_name')
        self.assertEqual(bh._BucketHandler__bucket_name, 'kvs-bucket_type')
        self.assertEqual(bh._BucketHandler__endpoint_url, 'https://hb.bizmrg.com')

    def test_upload_file(self):
        bucket_handler.boto3 = fake_boto3 = FakeBoto3()
        bh = BucketHandler(
            'aws_access_key_id',
            'aws_secret_access_key',
            'bucket_type',
            'specific_storage_name',
        )
        bh.upload_file('path_to_file_on_pc')
        fake_boto3._session.client().upload_file.assert_called_once_with(
            'path_to_file_on_pc',
            'kvs-bucket_type',
            'specific_storage_name/path_to_file_on_pc',
        )

    def test_get_public_link(self):
        bucket_handler.boto3 = fake_boto3 = FakeBoto3()
        bh = BucketHandler(
            'aws_access_key_id',
            'aws_secret_access_key',
            'bucket_type',
            'specific_storage_name',
        )
        bh.get_public_link('path_to_file_on_cloud')
        fake_boto3._session.client().generate_presigned_url.assert_called_once_with(
            'get_object',
            Params={
                'Bucket': 'kvs-bucket_type',
                'Key': 'path_to_file_on_cloud',
            },
            ExpiresIn=36000000,
        )

    def test_delete_file(self):
        bucket_handler.boto3 = fake_boto3 = FakeBoto3()
        bh = BucketHandler(
            'aws_access_key_id',
            'aws_secret_access_key',
            'bucket_type',
            'specific_storage_name',
        )
        fake_boto3._session.client().head_object.return_value = {
            'ResponseMetadata': {
                'HTTPStatusCode': 200,
            },
        }
        bh.delete_file('path_to_file_on_cloud')
        fake_boto3._session.client().head_object.assert_called_once_with(
            Bucket='kvs-bucket_type',
            Key='path_to_file_on_cloud',
        )
        fake_boto3._session.client().delete_object.assert_called_once_with(
            Bucket='kvs-bucket_type',
            Key='path_to_file_on_cloud',
        )
