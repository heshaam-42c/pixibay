#! /bin/sh

# This script is used to delete users from the Pixi API
pixiAPIEndpoint="https://photo-demo.westeurope.cloudapp.azure.com/hesh/api"

#delete admin user
token=$(curl -s -X POST -d '{"user": "useradmin@acme.com","pass": "hellopixi"}' -H 'Content-Type: application/json' $pixiAPIEndpoint/user/login | jq -r '.token')
userId=$(curl -s -X POST -d '{"user": "useradmin@acme.com","pass": "hellopixi"}' -H 'Content-Type: application/json' $pixiAPIEndpoint/user/login | jq -r '._id')
curl -s -X DELETE -H 'x-access-token: '$token $pixiAPIEndpoint/admin/user/$userId
echo "\nUser: useradmin@acme.com deleted"

#delete scan user
token=$(curl -s -X POST -d '{"user": "userscan-run@acme.com","pass": "hellopixi"}' -H 'Content-Type: application/json' $pixiAPIEndpoint/user/login | jq -r '.token')
userId=$(curl -s -X POST -d '{"user": "userscan-run@acme.com","pass": "hellopixi"}' -H 'Content-Type: application/json' $pixiAPIEndpoint/user/login | jq -r '._id')
curl -s -X DELETE -H 'x-access-token: '$token $pixiAPIEndpoint/admin/user/$userId
echo "\nUser: userscan-run@acme.com deleted"