import pspring

pspring.Configuration.defaults({
    "pspring.aws.region":"us-east-2",
    "pspring.aws.dynamodb.ttl":"3600",
    "pspring.aws.secretsMngr.secretId":"",
    "pspring.aws.secretsMngr.appSyncApiId":""
})
