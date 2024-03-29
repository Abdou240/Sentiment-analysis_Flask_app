import requests
from requests.auth import HTTPBasicAuth

# Define user credentials
users = [
    {"username": "Amber", "password": "9274"},
    {"username": "Rhonda", "password": "6818"},
    {"username": "Lamar", "password": "6478"},
    {"username": "Ulla", "password": "3610"},
]

# Define a sample sentence for sentiment analysis
sample_sentence = "This is a wonderful day!"

# Loop through each user
for user in users:
    print(f"User: {user['username']}")
    
    # /status (GET)
    response = requests.get('http://localhost:5000/status')
    print("Status:", response.text)

    # /welcome (GET)
    response = requests.get('http://localhost:5000/welcome', params={'username': user['username']})
    print("Welcome:", response.text)

    # /permissions (POST)
    response = requests.post('http://localhost:5000/permissions', auth=HTTPBasicAuth(user['username'], user['password']))
    print("Permissions:", response.json())
    
    # Attempt to use /v1/sentiment (POST)
    response_v1 = requests.post('http://localhost:5000/v1/sentiment', data={'sentence': sample_sentence}, auth=HTTPBasicAuth(user['username'], user['password']))
    if response_v1.ok:
        print("/v1/sentiment response:", response_v1.json())
    else:
        print("/v1/sentiment response: Access denied or error")
    
    # Attempt to use /v2/sentiment (POST)
    response_v2 = requests.post('http://localhost:5000/v2/sentiment', data={'sentence': sample_sentence}, auth=HTTPBasicAuth(user['username'], user['password']))
    if response_v2.ok:
        print("/v2/sentiment response:", response_v2.json())
    else:
        print("/v2/sentiment response: Access denied or error")
    
    print("\n" + "="*50 + "\n")
