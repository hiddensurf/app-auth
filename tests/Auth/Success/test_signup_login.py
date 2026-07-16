def test_login_success(client,user_data):
    data=user_data
    response_signup=client.post("/signup",json=data)
    assert response_signup.status_code == 201
    signup_body=response_signup.json()
    assert "id" in signup_body
    assert signup_body["full_name"]==data["full_name"]
    assert signup_body["user_name"]==data["user_name"]
    assert signup_body["email"]==data["email"]
    assert "password" not in signup_body
    assert "hashed_password" not in signup_body
    response_login=client.post("/token",data={"username":data['user_name'],
                                              "password":data['password']})
    assert response_login.status_code == 200
    login_body=response_login.json()
    assert "access_token" in login_body
    assert "token_type" in login_body
    assert type(login_body["access_token"]) == str
    assert login_body["token_type"] == "bearer"
