import boto3


class S3Client:
    def __init__(self, region="us-east-2"):
        self.region = region
        self.client = boto3.client("s3", region_name=region)
