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


## Updates
Please find my overall coding steps,
1. Project name fucus and app name orgapp
2. Installed DRF, JWT to handle the requirements. All the modules are mentioned in the requirements.txt
3. Added rest_framework, rest_framework_simplejwt and orgapp on the settings INSTALLED_APPS
4. Added a few more REST configurations like REST_FRAMEWORK, AUTH_USER_MODEL and SIMPLE_JWT.
5. models.py --> Main table component, overridden django builtin User model by inheriting AbstractUser and PermissionMixin.
6. Created separate urls.py under orgapp and wired the orgapp.urls in parent urls.py. Mentioned prefix as 'api/' in parent urls.py for orgapp. So that all the api will be prefixed in one place.
7. Created serializers.py and managers.py to handle the request and validation.
8. Created 3 kind of views, 
views.py -> to handle auth register, login and groups.
userviews.py -> to handle the user related api views
orgviews.py -> to handle organization related api views
otherviews.py -> to handle the info api views.
9. All are Class Based View and tested end to end. All API will respond with proper status code and json response.
