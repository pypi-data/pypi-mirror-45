from pspring import ConfigurationProvider, Configuration
from .secretsmngr import SecretsManager
import logging,json

logger = logging.getLogger(__name__)
config = Configuration.getConfig(__name__)

class SecretsMgrConfigProvider(ConfigurationProvider):
    def __init__(self,**kargs):
        secretId = kargs.get("secretId") or config.getProperty("secretId")
        region = kargs.get("region") or config.getProperty("region")

        self.mgr = SecretsManager(secretId=secretId,region=region)

    def getProperty(self,propertyName):
        secretValue = self.mgr.getSecretValue()
        return secretValue.get(propertyName)
