from tests.conftest import client

def test_should_status_code_ok(client):
	response = client.get('/prediction/predict/1/pungent/urban/brown/bruises/')
	assert response.status_code == 200

def test_json_response_ok(client):
	response = client.get('/prediction/predict/1/pungent/urban/brown/bruises/')
	data = response.data.decode()

	if '{"prediction":' in data:
		answer='ok'
	else:
		answer='ko'
	print(data)	

	assert answer == 'ok'

def test_json_response_poisoned(client):
	response = client.get('/prediction/predict/1/pungent/urban/brown/bruises/')
	data = response.data.decode()

	if 'poisoned' in data:
		answer='ok'
	else:
		answer='ko'
	print(data)	
	
	assert answer == 'ok'