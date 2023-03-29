# fucusdjango
Built the full fledge end to end API to handle the user and organization

http://localhost:8000/api/auth/register/ --> POST

Sample Payload:
{
    "name": "Gopi",
    "phone": "123456789",
    "email": "abcde@gmail.com",
    "organization": "Test",
    "birthdate": "2020-01-01",
    "password": "abc"
}

http://localhost:8000/api/auth/login/ -> POST

Payload
{
    "email": "abcde@gmail.com",
    "password": "abc"
}

http://localhost:8000/api/auth/groups/ --> GET

http://localhost:8000/api/users/  --> GET
--> Header should have the Token

http://localhost:8000/api/users/<nit:id>/ --> GET, POST, PATCH an DELETE
--> Header should have the Token

http://localhost:8000/api/info/ --> GET
--> Header should have the Token

http://localhost:8000/api/organizations/<int:id>/ --> GET, PATCH
--> Header should have the Token

http://localhost:8000/api/organizations/<int:id>/users/ --> GET
--> Header should have the Token

http://localhost:8000/api/organizations/<int:org_id>/users/<int:user_id>/ --> GET
--> Header should have the Token
