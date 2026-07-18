from faker import Faker
fake = Faker()
#email validation
def test_email(client,user_data_factory):
    user_1=user_data_factory()
    user_1['email'] = "examplegmail.com"
    response = client.post('/signup',json=user_1)
    assert response.status_code == 422
    body1 = response.json()
    assert "detail" in body1
    detail = body1['detail'][0]
    assert 'valid email address' in detail['msg']
    assert detail['loc'] == ['body','email']
    assert detail['ctx']['reason'] == 'An email address must have an @-sign.'
    user_2=user_data_factory()
    user_2['email'] = "@gmail.com"
    response = client.post('/signup',json=user_2)
    assert response.status_code == 422
    body2 = response.json()
    assert "detail" in body2
    detail = body2['detail'][0]
    assert 'valid email address' in detail['msg']
    assert detail['loc'] == ['body','email']
    assert detail['ctx']['reason'] == 'There must be something before the @-sign.'
#password validation
def test_password_too_short(client,user_data_factory):
    user=user_data_factory()
    user["password"]="notvalid123"
    response=client.post("/signup",json=user)
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    detail = body['detail'][0]
    assert "too_short" in detail["type"]
    assert detail['loc'] == ['body','password']
    assert "at least" in detail['msg']
#request body validation
def test_no_request_body(client):
    response=client.post("/signup")
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    detail = body["detail"][0]
    assert detail["type"] == "missing"
    assert detail["loc"] == ["body"]
    assert detail['msg'] == 'Field required'
def test_all_fields_missing(client):
    response=client.post("/signup",json={})
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    full_name_det=body["detail"][0]
    user_name_det=body["detail"][1]
    email_det=body["detail"][2]
    password_det=body["detail"][3]
    assert full_name_det["type"] == "missing"
    assert full_name_det["loc"] == ['body', 'full_name']
    assert full_name_det['msg'] == "Field required"
    assert user_name_det["type"] == "missing"
    assert user_name_det["loc"] == ['body', 'user_name']
    assert user_name_det['msg'] == "Field required"
    assert email_det["type"] == "missing"
    assert email_det["loc"] == ['body', 'email']
    assert email_det['msg'] == "Field required"
    assert password_det["type"] == "missing"
    assert password_det["loc"] == ['body', 'password']
    assert password_det['msg'] == "Field required"

    