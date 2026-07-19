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
def test_get_users_params_set(client,user_data_factory):
    for _ in range(10):
        user_to_add=user_data_factory()
        client.post("/signup",json=user_to_add)
    user=user_data_factory()
    client.post("/signup",json=user)
    register_user=user
    response_1=client.post("/token", data={"username":register_user["user_name"],"password":register_user["password"]})
    response_for_access_token=response_1.json()
    assert "access_token" in response_for_access_token and isinstance(response_for_access_token["access_token"],str)
    token=response_for_access_token["access_token"]
    response_all=client.get("/user",headers={"Authorization":f"Bearer {token}"})
    assert response_all.status_code == 200
    response_all_body=response_all.json()
    assert isinstance(response_all_body,list)
    total_length=len(response_all_body)
    to_check=response_all_body[total_length-10:]
    offset_int = total_length - 10
    response_3=client.get("/user",headers={"Authorization":f"Bearer {token}"},params={"offset":offset_int})
    assert response_3.status_code == 200
    response_3_body=response_3.json()
    assert isinstance(response_3_body,list)
    assert [u["id"] for u in to_check] == [u["id"] for u in response_3_body]


    