import logging

import boto3
from botocore.client import Config

logger = logging.getLogger(__name__)

class S3Client:
    def __init__(
            self, 
            endpoint_url: str, 
            access_key: str, 
            secret_key: str, 
            region_name: str = 'us-east-1'
        ):
        """Initialize S3 client."""
        self.s3_client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version='s3v4'),
            region_name=region_name
        )

    def bucket_exists(self, bucket_name):
        """Check if bucket exists."""
        buckets = self.s3_client.list_buckets()
        return any(bucket['Name'] == bucket_name for bucket in buckets['Buckets'])

    def create_bucket(self, bucket_name):
        """Create a new bucket."""
        if not self.bucket_exists(bucket_name):
            self.s3_client.create_bucket(Bucket=bucket_name)
            logger.info(f"Bucket '{bucket_name}' created")
        else:
            logger.info(f"Bucket '{bucket_name}' already exists")

    def get_object(self, bucket_name, object_name):
        """Get object from bucket."""
        return self.s3_client.get_object(Bucket=bucket_name, Key=object_name)

    def upload_object(self, file_path, bucket_name, object_name):
        """Upload object to bucket."""
        self.s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"'{file_path}' is successfully uploaded as '{object_name}' to bucket '{bucket_name}'")

    def download_file(self, bucket_name, object_name, file_path):
        """Download object from bucket."""
        self.s3_client.download_file(bucket_name, object_name, file_path)
        logger.info(f"'{object_name}' is successfully downloaded as '{file_path}' from bucket '{bucket_name}'")
    
    def delete_object(self, bucket_name, object_name):
        """Delete object from bucket."""
        self.s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        logger.info(f"'{object_name}' is successfully deleted from bucket '{bucket_name}'")

# NOTE: Example usage
# s3_client = S3Client(
#     endpoint_url='https://play.min.io',
#     access_key='YOUR-ACCESSKEYID',
#     secret_key='YOUR-SECRETACCESSKEY'
# )

# bucket_name = "my-bucket"
# s3_client.create_bucket(bucket_name)

# file_path = "/path/to/your/file.txt"
# s3_client.upload_file(file_path, bucket_name, "file.txt")
