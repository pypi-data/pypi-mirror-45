from pspring import ConfigurationProvider
from realtimeawssecretsmngr import RealTimeAwsSecretsMngr

from .defaultvars import secretId,region,apiId,logger

class RealTimeSecretsMgrConfigProvider(ConfigurationProvider):
    def __init__(self,**kargs):
        secretId = kargs.get("secretId") if kargs.get("secretId") else secretId
        region = kargs.get("region") if kargs.get("region") else region
        apiId = kargs.get("apiId") if kargs.get("apiId") else apiId

        self.mgr = RealTimeAwsSecretsMngr(secretId=secretId,apiId=apiId,region=region)
        self.mgr.subscribe(self.eventCallBack)

    def eventCallBack(self,response):
        logger.info("Received updated secret "+str(response))
        self.response = response

    def getProperty(propertyName):
        return self.response.get(propertyName)
