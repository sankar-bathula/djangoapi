from django.test import TestCase
import requests
import json
# Create your tests here.
BASE_URL = 'http://127.0.0.1:8000/'
END_POINT = 'api/'
def get_resource(id=None):
    data = {}
    if id is not None:
        data = {
        'id':id
        }
    resp = requests.get(BASE_URL + END_POINT, data = json.dumps(data))
    print(resp.status_code)
    print(resp.json())
def create_resource():
	new_data={
	'eno': 222,
	'ename':'Bathula Babu',
	'esal':50000,
	'eaddr':'Kanigiri',
	}
	r=requests.post(BASE_URL + END_POINT, data=json.dumps(new_data))
	print(r.status_code)
	print(r.text)
	print(r.json)
#create_resource()

def update_resource(id=None):
	new_data={
	'id':id,
	'eno': 123,
	'ename':'Bathula Sankar Babu',
	'esal':50000,
	'eaddr':'Prakasam',
	}
	r=requests.put(BASE_URL + END_POINT, data=json.dumps(new_data))
	print(r.status_code)
	print(r.text)
	print(r.json)

def delete_resource(id=None):
	new_data={
	'id':id,
	}
	r=requests.delete(BASE_URL + END_POINT, data=json.dumps(new_data))
	print(r.status_code)
	print(r.text)
	print(r.json)
delete_resource(4)