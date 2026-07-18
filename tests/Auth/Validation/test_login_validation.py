#no form data
def test_no_data(client):
    response=client.post("/token")
    assert response.status_code == 422
    body=response.json()
    assert "detail" in body
    username_error=body["detail"][0]
    password_error=body["detail"][1]
    assert username_error["type"] == "missing" 
    assert password_error["type"] == "missing"
    assert username_error["msg"] == "Field required" 
    assert password_error["msg"] == "Field required"
    assert username_error['loc'][1] == 'username' 
    assert password_error['loc'][1] == 'password'