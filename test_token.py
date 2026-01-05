import json
import urllib.request

url = 'http://127.0.0.1:8000/api/token/'
data = json.dumps({'username': 'testsec', 'password': 'pass'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    print(result)