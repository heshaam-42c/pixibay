#! /bin/sh

docker_yaml=docker-compose.yaml

if [ "$1" == "-h" ]; then
    echo "usage: $0 [build|down|db-reset|db-down]\n"
    echo "This script is used to manage the Pixi application"
    echo "   -h          Show this help message"
    echo "   build       Build the Pixi application"
    echo "   down        Shut down the Pixi application"
    echo "   db-reset    Reset the Pixi database"
    echo "   db-down     Shut down the Pixi database"
    exit 0
fi

if [ $# -lt 1 ]; then
    echo "Starting Pixi..."
    docker-compose -f $docker_yaml down
    docker-compose -f $docker_yaml up -d
    sleep 3
fi

if [ "$1" == "build" ]; then
    echo "Building Pixi..."
    docker-compose -f $docker_yaml down
    docker-compose -f $docker_yaml up -d --build
    sleep 3
fi

if [ "$1" == "down" ]; then
    echo "Shutting down Pixi..."
    docker-compose -f $docker_yaml down
    exit 0
fi

if [ "$1" == "db-reset" ]; then
    echo "Stopping PixiDB..."
    docker-compose down db
    echo "Creating PixiDB"
    docker-compose up -d db
fi

if [ "$1" == "db-down" ]; then
    echo "Stopping PixiDB..."
    docker-compose down db
    exit 0
fi

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

# Save only the response code
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

# DEBUG: Save entire response
# curl_response_inbound=$(curl -s -o /dev/null -D - POST -H "Content-Type: application/json" -d "$json_data_user_inbound" "$api_register_url")
# curl_response_common=$(curl -s -o /dev/null -D - POST -H "Content-Type: application/json" -d "$json_data_user_common" "$api_register_url")

# echo "Inbound User \n$curl_response_inbound"
# echo "Common User \n$curl_response_common"