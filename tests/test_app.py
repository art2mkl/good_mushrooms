from tests.conftest import client

def test_should_status_code_ok(client):
	response = client.get('/test')
	assert response.status_code == 200

def test_server_response(client):
	response = client.get('/test')
	data = response.data.decode()
	print(data)
	assert data == 'Test Serveur'