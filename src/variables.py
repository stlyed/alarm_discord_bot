#!/usr/bin/env python3
import hashlib
import boto3

active_alarms_file = 'active_alarms.csv'
active_alarms_dup_file = 'active_alarms-dup.csv'


def get_secret(code_secret):
    secret_name = "Alarm_Discord_Bot"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager',
                            region_name=region_name)

    # Get every secret stored
    response = str(client.get_secret_value(SecretId=secret_name))
    response = response[response.find('SecretString'):response.find('}') + 1]

    # only return the secret that is asked for
    secret_value = [i for i in range(len(response)) if response.startswith('"', i)]
    x, y = 0, 1
    for secrets in range(int(len(secret_value) / 2)):
        if response[secret_value[x] + 1:secret_value[y]] == code_secret:
            return response[secret_value[x + 2] + 1:secret_value[y + 2]]
        x += 4; y += 4


# generate an unique ID for each alarm based on the alarm specs
def generate_alarm_id(user_alarm):
    m = hashlib.md5()
    m.update(str(user_alarm).encode())
    return str(int(m.hexdigest(), 16))[:12]
