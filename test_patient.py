import json
import urllib.request

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY3NjUwMzc0LCJpYXQiOjE3Njc2NDY3NzQsImp0aSI6IjM3MmM0MGU2ZGIzZDQzN2Q5ZWE4ZjZlYzk2MmFhNDBkIiwidXNlcl9pZCI6IjIifQ.mgVjuuCK2h5-Zm8e10PBH9kc60VhqocxvXz9dt1ZjQM'
url = 'http://127.0.0.1:8000/api/patients/'
data = json.dumps({
    'nom': 'Doe',
    'prenom': 'John',
    'date_naissance': '1990-01-01',
    'sexe': 'M',
    'telephone': '123456789',
    'adresse': '123 Main St',
    'contact_urgence': 'Jane Doe'
}).encode('utf-8')
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
}
req = urllib.request.Request(url, data=data, headers=headers, method='POST')
with urllib.request.urlopen(req) as response:
    result = json.loads(response.read().decode('utf-8'))
    print('Created patient:', result)

# Now list patients
req_list = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req_list) as response:
    result = json.loads(response.read().decode('utf-8'))
    print('Patients list:', result)