def test_get_users(client, user_data_factory):
    user=user_data_factory()
    client.post("/signup",json=user)
    response_1=client.post("/token", data={"username":user["user_name"],"password":user["password"]})
    response_1_body=response_1.json()
    assert "access_token" in response_1_body and isinstance(response_1_body["access_token"],str)
    token=response_1_body["access_token"]
    response_2=client.get("/user",headers={"Authorization":f"Bearer {token}"})
    assert response_2.status_code == 200
    response_2_body=response_2.json()
    assert isinstance(response_2_body,list)
    created_user=next(u for u in response_2_body 
                      if u["user_name"] == user["user_name"])
    assert created_user["full_name"] == user["full_name"]
    assert created_user["email"] == user["email"]
    assert "id" in created_user

    