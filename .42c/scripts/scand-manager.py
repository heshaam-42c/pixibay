#!/usr/bin/env python3

import json
import argparse
import requests
import sys
import random

# This calls the scand-manager API to start a scan job
def start_job (scanToken: str, targetAPIToken: str):
    url =  "https://photo-demo.westeurope.cloudapp.azure.com/scand/api/job"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    
    job_id = random.randint(1, 9999)
    job_name = "scand-job-"+str(job_id)

    payload = {f"token": scanToken, "name": job_name, "expirationTime": 600, "platformService": "services.demolabs.42crunch.cloud:8001", "scandImage": "42crunch/scand-agent:v2", "env": {"SCAN42C_SECURITY_ACCESS_TOKEN": targetAPIToken, "SCAN42C_HOST": "https://photo-demo.westeurope.cloudapp.azure.com/hesh/api"}}
    response = requests.post(url, data=json.dumps(payload), headers=headers) 

    return response.json()

def main():

    scanToken = sys.argv[1]
    targetAPIToken = sys.argv[2]

    scan_job = start_job (scanToken, targetAPIToken)

    print (scan_job)

# -------------- Main Section ----------------------
if __name__ == '__main__':
    main()