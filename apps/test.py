import requests
import json


headers = {
    'user_agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
    'Ocp-Apim-Subscription-Key' : 'c13c3a8e2f6b46da9c5c425cf61fab3e'
}


res = requests.get('https://apim.laliga.com/public-service/api/v1/teams?subscriptionSlug=laliga-santander-2019&limit=99&offset=0&orderField=nickname&orderType=ASC',headers=headers)
