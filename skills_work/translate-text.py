# -*- coding: utf-8 -*-
import requests, uuid, json


def translate(text):
    subscription_key = "33c4d5bb255a4719b12c2e3a3c74c163"
    endpoint = "https://translator-sea.cognitiveservices.azure.com/sts/v1.0/issuetoken"

    path = '/translate?api-version=3.0'
    params = '&to=en'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text    
    }]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    print(json.dumps(response, sort_keys=True, indent=4,
                     ensure_ascii=False, separators=(',', ': ')))


if __name__ == '__main__':
    translate('привіт')