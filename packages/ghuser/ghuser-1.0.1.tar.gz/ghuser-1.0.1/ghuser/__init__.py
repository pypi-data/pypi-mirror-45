import requests
import json

def get(username):
    endpoint = 'https://api.github.com/users/' + username
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()

    data = response.json()

    result = {}

    result['username'] = data['login']
    result['bio'] = data['bio']
    result['company'] = data['company']
    result['location'] = data['location']
    result['repos'] = data['public_repos']
    result['followers'] = data['followers']
    result['following'] = data['following']
    result['website_url'] = data['blog']
    result['id'] = data['id']
    result['avatar_url'] = data['avatar_url']
    result['web_url'] = data['html_url']

    return result
