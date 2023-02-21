import os, json
import pickle

# from django.forms import ValidationError
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from project_schema import (
    UserSchema,
    TeamSchema,
    repopulate_un_path,
)
from django.views.decorators.csrf import csrf_exempt
from .views import db_path, team_path


@api_view(["POST"])
@csrf_exempt
def create_user(request) -> str:
    req_body = json.loads(request.body)
    try:
        data = UserSchema().load(req_body)
    except ValidationError as e:
        return JsonResponse({"message": e.message, "status_code": 500})
    with open(db_path, "ab") as ap:
        pickle.dump(data, ap)
    return JsonResponse({"id": data["id"]})


@api_view(["GET"])
@csrf_exempt
def list_users(request) -> str:
    user_list = []
    with open(db_path, "rb") as ap:
        while True:
            try:
                user_list.append(UserSchema().dump(pickle.load(ap)))
            except EOFError:
                break
    return JsonResponse(json.dumps(user_list), safe=False)


@api_view(["GET"])
@csrf_exempt
def describe_user(request) -> str:
    user_dict = {}
    req_body = json.loads(request.body)
    with open(db_path, "rb") as ap:
        while True:
            try:
                user_dict = pickle.load(ap)
                if user_dict["id"] == req_body["id"]:
                    user_dict.pop("id")
                    user_dict.pop("display_name")
                    break
                else:
                    user_dict = {}
            except EOFError:
                break

    if not user_dict:
        return JsonResponse({"message": "User Not Found", "status_code": 404})

    return JsonResponse(user_dict)


@api_view(["PATCH"])
@csrf_exempt
def update_user(request) -> str:
    user_list = []
    un_list = []
    req_body = json.loads(request.body)
    with open(db_path, "rb") as ap:
        while True:
            try:
                user_dict = pickle.load(ap)
                if user_dict["id"] == req_body["id"]:
                    user_det = json.loads(req_body["user"])
                    user_dict["name"] = user_det["name"]
                    user_dict["display_name"] = user_det["display_name"]
                data = TeamSchema().load(user_dict)
                un_list.append(user_dict["name"])
                user_list.append(data)
            except EOFError:
                break
            except ValidationError as e:
                return JsonResponse({"message": e.message, "status_code": 500})

    os.remove(db_path)

    # repopulates usernames pickle
    repopulate_un_path(un_list)
    with open(db_path, "ab") as ap:
        for user in user_list:
            pickle.dump(user, ap)

    return JsonResponse({"message": "User updated"})


@api_view(["GET"])
@csrf_exempt
def get_user_teams(request):
    teams_list = []
    req_body = json.loads(request.body)
    with open(team_path, "rb") as ap:
        while True:
            try:
                team_dict = pickle.load(ap)
                if req_body["id"] in team_dict["users"]:
                    team_dict.pop("id")
                    team_dict.pop("users")
                    team_dict["creation_time"] = str(team_dict["creation_time"])
                    teams_list.append(team_dict)
            except EOFError:
                break

    return JsonResponse(json.dumps(teams_list), safe=False)
