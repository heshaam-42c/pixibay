#! /bin/sh

if [ $# -lt 1 ]; then
    echo "Starting Pixi"
    docker-compose down
    docker-compose up -d
fi

if [ "$1" == "build" ]; then
    echo "Building Pixi"
    docker-compose down
    docker-compose up -d --build
fi

sleep 5

echo "Creating Users..."

# JSON data for the API request 
json_data_user_inbound='{"user": "scanuser@test.com","pass": "hellopixi","name": "Scan Test User","is_admin": false,"account_balance": 1000}'
json_data_user_common='{"user": "attacks-demo@acme.com","pass": "hellopixi","name": "Attack User","is_admin": false,"account_balance": 1000}'

# Invoke the API using curl with POST method and passing the JSON data
api_url="http://localhost:8090/api/user/register"
curl_response_inbound=$(curl -s -X POST -H "Content-Type: application/json" -d "$json_data_user_inbound" "$api_url")
curl_response_common=$(curl -s -X POST -H "Content-Type: application/json" -d "$json_data_user_common" "$api_url")