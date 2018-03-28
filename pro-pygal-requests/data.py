# coding:utf-8

import requests
import json

url = "https://github.com/search?utf8=%E2%9C%93&q=python"


response = requests.get(url, stream=True)
# i = Image.open(BytesIO(response.content))
print(response.text)
# print(response.__dict__)
# print("status code:", response.status_code)
# print("header:", response.headers)
# print("encoding:", response.encoding)
# print("text:", response.text)
# print("cookies:", response.cookies)
