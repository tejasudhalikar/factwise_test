"""teamprojectplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import user_view, project_board_view, team_view


urlpatterns = [
    path("create/user", user_view.create_user, name="Create user"),
    path("users", user_view.list_users, name="List users"),
    path("user", user_view.describe_user, name="Get user"),
    path("update/user", user_view.update_user, name="Update user"),
    path("create/team", team_view.create_team, name="Create team"),
    path("update/team", team_view.update_team, name="Create team"),
    path("teams", team_view.list_teams, name="List teams"),
    path("team", team_view.describe_team, name="Get team"),
    path("team/add", team_view.add_users_to_team, name="Add users to team"),
    path(
        "team/remove", team_view.remove_users_from_team, name="Remove users from team"
    ),
    path("team/users", team_view.list_team_users, name="List users from team"),
    path("user/teams", user_view.get_user_teams, name="List teams of user"),
    path("create/board", project_board_view.create_board, name="Create board"),
    path("board/close", project_board_view.close_board, name="Close board"),
    path("task/add", project_board_view.add_task, name="Add task"),
    path("task/close", project_board_view.update_task_status, name="Add task"),
    path("boards", project_board_view.list_boards, name="List boards"),
    path("export", project_board_view.export_board, name="Export board"),
]
