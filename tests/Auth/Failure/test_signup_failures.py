from conftest import fake
def test_email_exists(client,user_data_factory):
    user1=user_data_factory()
    fake_email=fake.email()
    user1["email"] = fake_email
    client.post('/signup', json=user1)
    user2 = user_data_factory()
    user2["email"] = fake_email
    response=client.post('/signup',json=user2)
    assert response.status_code == 409
    body = response.json()
    assert "detail" in body
    assert body["detail"] == "Email already exists"
def test_username_exists(client, user_data_factory):
    user1=user_data_factory()
    fake_username=fake.user_name()
    user1["user_name"] = fake_username
    client.post("/signup", json=user1)
    user2=user_data_factory()
    user2["user_name"] = fake_username
    response=client.post("/signup", json=user2)
    assert response.status_code ==409
    body = response.json()
    assert "detail" in body
    assert body["detail"] == "Username already taken"