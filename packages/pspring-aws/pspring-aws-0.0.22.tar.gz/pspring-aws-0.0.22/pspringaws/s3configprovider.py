from pspring import ConfigurationProvider, Configuration
import logging,json

import boto3

logger = logging.getLogger(__name__)
config = Configuration.getConfig(__name__)

class S3ConfigProvider(ConfigurationProvider):
    def __init__(self,**kargs):
        self.bucketId = kargs.get("bucketId") or config.getProperty("bucketId")
        self.objectKey = kargs.get("objectKey") or config.getProperty("objectKey")
        self.region = kargs.get("region") or config.getProperty("region")

        client = boto3.client("s3",region_name=self.region)
        file = client.get_object(Bucket=self.bucketId,Key=self.objectKey)
        filecontent = file.get("Body").read().decode("utf-8")
        try:
        	self.config = json.loads(str(filecontent))
        except Exception as er:
        	logger.warn(f"Received content from s3 was not json {er}")

    def getProperty(self,propertyName):
        return self.config.get(propertyName)
