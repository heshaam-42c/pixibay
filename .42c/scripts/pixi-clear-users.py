#!/usr/bin/env python3

import json
import argparse
import requests
import sys
#import subprocess
import os


# This call updates a named scan configuration
def obtain_token (name: str, password: str):
    url =  f"{TARGET_URL}/user/login"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    
    #Initialize  token value
    user_token = None

    payload = {f"user": name, "pass": password}
    response = requests.post(url, data=json.dumps(payload), headers=headers) 

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        sys.exit(1)
    else:
        user_token = response.json().get('token')
        return user_token

def obtain_users (token: str):
    url =  f"{TARGET_URL}/admin/all_users"
    headers = {"accept": "application/json", "x-access-token": token}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        sys.exit(1)
    else:
        pixiUsers = response.json()
        return pixiUsers


def main():
    parser = argparse.ArgumentParser(
        description='Pixi API Login'
    )
    parser.add_argument('-u', "--user-name",
                        default="UserName",
                        help="PixiApp User", required=True)
    parser.add_argument('-p', "--user-pass",
                        help="PixiApp Password", required=True)
    parser.add_argument('-t', '--target', 
                        required=False, 
                        default='https://photo-demo.westeurope.cloudapp.azure.com/api', 
                        help="Default is https://photo-demo.westeurope.cloudapp.azure.com/api",
                        type=str)
    parsed_cli = parser.parse_args()

    global TARGET_URL

    user = parsed_cli.user_name
    password = parsed_cli.user_pass
    TARGET_URL = parsed_cli.target

    pixiApprovedUsers = ["misty94@demo.mail", "pixiadmin@demo.mail", "barbara8@demo.mail", "scanuser@test.com", "attacks-demo@acme.com", "health@check.com"]

    user_token = obtain_token (user, password)
    print (user_token)

    pixiUsers = obtain_users(user_token)

    for user in pixiUsers:
        if user['email'] not in pixiApprovedUsers:
            print (f"Deleting email {user['email']} and id {user['_id']}")
            url =  f"{TARGET_URL}/admin/user/{user['_id']}"
            headers = {"accept": "application/json", "x-access-token": user_token}
            response = requests.delete(url, headers=headers) 

    echo = os.system("echo 'Cleaned up extra Pixi Users'")

# -------------- Main Section ----------------------
if __name__ == '__main__':
    main()
