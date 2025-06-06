#! /bin/sh

if [ "$1" == "down" ]; then
    echo "Stopping PixiDB..."
    docker-compose down db
    exit 0
fi

if [ "$1" == "clean" ]; then
    echo "Stopping PixiDB..."
    docker-compose down db
fi

echo "Creating PixiDB"
docker-compose up -d db

# Check if API is running
api_login_url="http://localhost:8090/api/user/login"
json_data_user_login='{"user": "misty94@demo.mail","pass": "ball"}'
curl_response_login=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$json_data_user_login" "$api_login_url")

if [ "$curl_response_login" == "200" ]; then
    echo "API is up and running"
else
    echo "API is not reachable, got $curl_response_invoke"
    exit 1
fi

echo "Creating Users..."

# JSON data for the API request 
json_data_user_inbound='{"user": "scanuser@test.com","pass": "hellopixi","name": "Scan Test User","is_admin": false,"account_balance": 1000}'
json_data_user_common='{"user": "attacks-demo@acme.com","pass": "hellopixi","name": "Attack User","is_admin": false,"account_balance": 1000}'

# Invoke the API using curl with POST method and passing the JSON data
api_register_url="http://localhost:8090/api/user/register"
curl_response_inbound=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$json_data_user_inbound" "$api_register_url")
curl_response_common=$(curl -s -o /dev/null -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$json_data_user_common" "$api_register_url")

if [ "$curl_response_inbound" == "200" ]; then
    echo "Inbound User Created"
else
    echo "Inbound User Creation Failed, got $curl_response_inbound"
fi

if [ "$curl_response_common" == "200" ]; then
    echo "Common User Created"
else
    echo "Common User Creation Failed, got $curl_response_common"
fi