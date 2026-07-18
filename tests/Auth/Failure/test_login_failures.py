#invalid form data
def test_invalid_username(client,registered_user):
    user=registered_user
    response=client.post("/token",data={"username":"fake_user_384587365876","password":user["password"]})
    assert response.status_code == 401
    body = response.json()
    assert "detail" in body
    assert body["detail"] == "Invalid username or password"
def test_invalid_password(client,registered_user):
    user=registered_user
    response=client.post("/token",data={"username":user["user_name"],"password":"fake_password_@^#H)IJQN';"})
    assert response.status_code == 401
    body = response.json()
    assert "detail" in body
    assert body["detail"] == "Invalid username or password"
