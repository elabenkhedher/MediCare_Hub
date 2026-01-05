import json
import urllib.request

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3NjUwMzc0LCJpYXQiOjE3Njc2NDY3NzQsImp0aSI6IjM3MmM0MGU2ZGIzZDQzN2Q5ZWE4ZjZlYzk2MmFhNDBkIiwidXNlcl9pZCI6IjIifQ.mgVjuuCK2h5-Zm8e10PBH9kc60VhqocxvXz9dt1ZjQM'
url = 'http://127.0.0.1:8000/api/dossier-medical/'
headers = {
    'Authorization': f'Bearer {token}'
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    print('DossierMedical list:', result)