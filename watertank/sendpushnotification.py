import requests

def sendpushnotification():
# Open bearer token file (not checked in to git. Contains only the Tibber bearer token
    with open('bearer.secret','r') as token_file:
        bearer_token = token_file.read().strip()

    url = "https://api.tibber.com/v1-beta/gql"
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + str(bearer_token)}

    with open('tibberpush.graphql','r') as query_file:
        mutation_query = query_file.read().strip()

    payload = {
        'query': mutation_query
    }

    response = requests.post(url=url, headers=headers, json=payload) 
    print("response status code: ", response.status_code)
    print(response.json())

sendpushnotification() 
