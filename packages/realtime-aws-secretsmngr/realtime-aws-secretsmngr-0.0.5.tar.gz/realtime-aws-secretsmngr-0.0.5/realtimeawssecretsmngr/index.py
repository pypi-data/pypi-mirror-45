import boto3
from appsyncclient import AppSyncClient
import os
import json

import logging

logger = logging.getLogger("realtime-aws-secretsmngr")

class RealTimeAwsSecretsMngr():
    def __init__(self,**kargs):
        self.region = kargs.get("region")
        self.secretId = kargs.get("secretId")

        if(self.secretId == None or self.region == None):
            logger.error("secretId and region required")
            raise Exception("configuration error")

        self.client = AppSyncClient(**kargs)
        self.botoclient = boto3.client("secretsmanager",region_name=self.region)

    def subscribe(self,callback):
        response = self.botoclient.get_secret_value(SecretId=self.secretId)
        secretString = response.get("SecretString")
        callback(secretString)

        secretString = secretString.replace("\"","\\\"")
        query = json.dumps({"query": "subscription {\n  updatedResource(id:\"arn:aws:secretsmanager:::"+self.secretId+"\") {\n    id\n    data\n  }\n}\n"})

        def secretcallback(client, userdata, msg):
            logger.debug("New data received : "+str(msg))
            callback(json.loads(msg.payload).get("data",{}).get("updatedResource",{}).get("data"))

        response = self.client.execute(data=query,callback=secretcallback)
