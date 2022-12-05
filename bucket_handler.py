import boto3


class BucketHandler:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str,
                 bucket_type: str, specific_storage_name: str) -> None:
        new_session = boto3.session.Session()
        self.specific_storage_name = specific_storage_name
        self.__bucket_name = "kvs-" + bucket_type
        self.__endpoint_url = "https://hb.bizmrg.com"
        self.__session = new_session.client(
            service_name="s3",
            endpoint_url=self.__endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def upload_file(self, path_to_file_on_pc: str):
        file_name = path_to_file_on_pc.split("/")[-1]
        self.__session.upload_file(path_to_file_on_pc, self.__bucket_name,
                                   f"{self.specific_storage_name}/" + file_name)

    def get_public_link(self, path_to_file_on_cloud: str) -> str:

        return self.__session.generate_presigned_url('get_object', Params={
            'Bucket': self.__bucket_name, 'Key':
                path_to_file_on_cloud}, ExpiresIn=36000000)

    def delete_file(self, path_to_file_on_cloud: str):
        resp = self.__session.head_object(Bucket=self.__bucket_name, Key=path_to_file_on_cloud)
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            self.__session.delete_object(Bucket=self.__bucket_name, Key=path_to_file_on_cloud)
        else:
            raise FileNotFoundError("File does not exist in bucket")
