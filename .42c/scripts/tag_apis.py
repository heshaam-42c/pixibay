#!/usr/bin/env python3

import json
import argparse
import requests
import sys
#import subprocess
import os


# This call fetches the tag id
def get_tag_id (token: str, category: str, tag: str):
    url =  f"{PLATFORM_URL}/api/v2/tags?readDependencies=yes
    headers = {"accept": "application/json", "X-API-KEY": token}

    response = requests.get(url, headers=headers) 

    tag_id = None

    if response.status_code != 200:
        sys.exit(1)
    else:
        for tag in response.json().get('list'):
            if tag.get('categoryName') == category and tag.get('tagName') == tag:
                tag_id = tag.get('id')
                break
        return tag_id


# This call tags the api
def tag_api (token: str, api_uuid: str, tag_id: str, category: str, tag: str):
    url =  f"{PLATFORM_URL}/api/v2/apis/{api_uuid}/tags/assign
    headers = {"accept": "application/json", "X-API-KEY": token}

    payload = {f"id": tag_id, "categoryName": category, "name": tag}
    response = requests.put(url, data=json.dumps(payload), headers=headers) 

    if response.status_code != 200:
        sys.exit(1)
    else:
        return response.json()

def main():
    parser = argparse.ArgumentParser(
        description='42Crunch API Tagging Script'
    )
    parser.add_argument('-u', "--api-uuid",
                        help="42Crunch API to tag", required=True)
    parser.add_argument('-c', "--category",
                        help="Category is a group of tags", required=True)
    parser.add_argument('-n', "--tag-name",
                        help="The tag name", required=True)
    parser.add_argument("-t", "--token", 
                        required=True, help="42Crunch API key")
    parser.add_argument('-p', '--platform', 
                        required=False, 
                        default='https://demolabs.42crunch.cloud', 
                        help="Default is https://demolabs.42crunch.cloud",
                        type=str)
    parsed_cli = parser.parse_args()

    global PLATFORM_URL

    api_uuid = parsed_cli.api_uuid
    category = parsed_cli.category
    tagName = parsed_cli.tag_name
    token = parsed_cli.token
    PLATFORM_URL = parsed_cli.platform

    #get tag id
    tag_id = get_tag_id (token, category, tagName)

    #tag the api
    tag_api_response = tag_api (token, api_uuid, tag_id, category, tagName)
    print (tag_api_response)

# -------------- Main Section ----------------------
if __name__ == '__main__':
    main()
