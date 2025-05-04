from app import models, schemas
import pytest
from app.routers import post,user
   
   
# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.status_code == 200
    


def test_create_user(client):
    res = client.post("/users/",json={"email":"cece@gmail.com","password":"paul1234"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "cece@gmail.com"
    assert res.status_code == 201
               

def test_login_user(client,test_user):
    res = client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    login_res = schemas.Token(**res.json())
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
               
               
def test_login_user_incorrect_password(client,test_user):
    res = client.post("/login",data={"username":test_user['email'],"password":"wrongpassword"})
    assert res.status_code == 403
    assert res.json().get("detail") == "Invalid Credentials"