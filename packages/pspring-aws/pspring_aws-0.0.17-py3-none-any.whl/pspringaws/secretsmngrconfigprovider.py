from pspring import ConfigurationProvider
from .secretsmngr import SecretsManager

from .defaultvars import secretId,region

class SecretsMgrConfigProvider(ConfigurationProvider):
    def __init__(self,**kargs):
        secretId = kargs.get("secretId") if kargs.get("secretId") else secretId
        region = kargs.get("region") if kargs.get("region") else region

        self.mgr = SecretsManager(secretId=secretId,region=region)

    def getProperty(propertyName):
        return self.mgr.getSecretValue().get(propertyName)
