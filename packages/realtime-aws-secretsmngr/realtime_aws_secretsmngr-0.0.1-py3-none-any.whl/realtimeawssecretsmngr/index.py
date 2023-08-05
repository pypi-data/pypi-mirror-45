import boto3
from appsyncclient import AppSyncClient
import os
regionDefault = os.environ.get("region","us-east-1")
import json

class RealTimeAwsSecretsMngr():
    def __init__(self,**kargs):
        self.client = AppSyncClient(authenticationType="API_KEY")
        self.region = kargs.get("region") if kargs.get("region") else regionDefault
        self.botoclient = boto3.client("secretsmanager",region_name=self.region)
        self.secretId = kargs.get("secretId")

    def subscribe(self,callback):
        response = self.botoclient.get_secret_value(SecretId=self.secretId)
        secretString = response.get("SecretString")
        callback(secretString)

        secretString = secretString.replace("\"","\\\"")
        query = json.dumps({"query": "subscription {\n  updatedSecret(id:\""+self.secretId+"\") {\n    id\n    secretString\n  }\n}\n"})

        def secretcallback(client, userdata, msg):
            callback(json.loads(msg.payload).get("data",{}).get("updatedSecret",{}).get("secretString"))

        response = self.client.execute(data=query,callback=secretcallback)
