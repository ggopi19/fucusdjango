from django.urls import path
from .views import (RegisterView, LoginView, GroupView)
from .userviews import UsersListView
from .orgviews import (OrgListView, OrgDetailsView, OrgDetailsLevelView)
from .otherviews import OtherView
urlpatterns = [
    # Register, Login and Groups
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/groups/', GroupView.as_view()),

    # User Endpoints
    path('users/', UsersListView.as_view()),
    path('users/<int:id>/', UsersListView.as_view()),

    # Organization Endpoints
    path('organizations/<int:id>/', OrgListView.as_view()),

    # Organization details Endpoints
    path('organizations/<int:id>/users/', OrgDetailsView.as_view()),

    # Organization details Level Endpoints
    path('organizations/<int:org_id>/users/<int:user_id>/', OrgDetailsLevelView.as_view()),

    # Other endpoint
    path('info/', OtherView.as_view()),
]
