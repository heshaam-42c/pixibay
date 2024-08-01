#! /bin/sh

# This script is used to add users to the Pixi API
pixiAPIEndpoint="https://photo-demo.westeurope.cloudapp.azure.com/hesh/api"

#Register the Scan test user
curl -s -X POST -d '{"user": "scanuser@test.com","pass": "hellopixi","name": "Scan Test User","is_admin": false,"account_balance": 975}' -H 'Content-Type: application/json' $pixiAPIEndpoint/user/register
echo "\nUser: scanuser@test.com added"

#Login and return token for the Scan test user
token=$(curl -s -X POST -d '{"user": "scanuser@test.com","pass": "hellopixi"}' -H 'Content-Type: application/json' $pixiAPIEndpoint/user/login | jq -r '.token')
echo "\nlogin token: $token\n"

#Register the Attack user
curl -s -X POST -d '{"user": "attacks-demo@acme.com","pass": "hellopixi","name": "Attack User","is_admin": false,"account_balance": 1000}' -H 'Content-Type: application/json' $pixiAPIEndpoint/user/register
echo "\nUser: attacks-demo@acme.com added"

#Login and return token for the Attack user
token=$(curl -s -X POST -d '{"user": "attacks-demo@acme.com","pass": "hellopixi"}' -H 'Content-Type: application/json' $pixiAPIEndpoint/user/login | jq -r '.token')
echo "\nlogin token: $token\n"