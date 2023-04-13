import requests

url = 'http://127.0.0.1:5000'
myobj = {"key":"value"}

text= "text"

x = requests.post(url, json = text)

print(x.text)
