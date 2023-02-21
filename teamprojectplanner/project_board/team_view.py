import os, json
import pickle

# from django.forms import ValidationError
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from project_schema import (
    TeamSchema,
    repopulate_tn_path,
    validate_user_ids,
)
from django.views.decorators.csrf import csrf_exempt
from .views import team_path, db_path


@api_view(["POST"])
@csrf_exempt
def create_team(request) -> str:
    req_body = json.loads(request.body)
    try:
        data = TeamSchema().load(req_body)
    except ValidationError as e:
        return JsonResponse({"message": e.message, "status_code": 500})
    with open(team_path, "ab") as ap:
        pickle.dump(data, ap)
    return JsonResponse({"id": data["id"]})


@api_view(["GET"])
@csrf_exempt
def list_teams(request) -> str:
    team_list = []
    with open(team_path, "rb") as ap:
        while True:
            try:
                team = pickle.load(ap)
                team.pop("id")
                team.pop("users")
                team["creation_time"] = str(team["creation_time"])
                team_list.append(team)
            except EOFError:
                break
    return JsonResponse(json.dumps(team_list), safe=False)


@api_view(["GET"])
@csrf_exempt
def describe_team(request) -> str:
    team_dict = {}
    req_body = json.loads(request.body)
    with open(team_path, "rb") as ap:
        while True:
            try:
                team_dict = pickle.load(ap)
                if team_dict["id"] == req_body["id"]:
                    team_dict.pop("id")
                    break
                else:
                    team_dict = {}
            except EOFError:
                break

    if not team_dict:
        return JsonResponse({"message": "Team Not Found", "status_code": 404})

    return JsonResponse(team_dict)


@api_view(["PATCH"])
@csrf_exempt
def update_team(request) -> str:
    team_list = []
    tn_list = []
    req_body = json.loads(request.body)
    with open(team_path, "rb") as ap:
        while True:
            try:
                team_dict = pickle.load(ap)
                if team_dict["id"] == req_body["id"]:
                    team_det = req_body["team"]
                    team_dict["name"] = team_det["name"]
                    team_dict["description"] = team_det["description"]
                    team_dict["admin"] = team_det["admin"]
                    data = TeamSchema().load(team_dict)
                tn_list.append(team_dict["name"])
                team_list.append(team_dict)
            except EOFError:
                break
            except ValidationError as e:
                return JsonResponse({"message": e.message, "status_code": 500})
    os.remove(team_path)
    repopulate_tn_path(tn_list)
    with open(team_path, "ab") as ap:
        for team in team_list:
            pickle.dump(team, ap)

    return JsonResponse({"message": "Team updated"})


@api_view(["PATCH"])
@csrf_exempt
def add_users_to_team(request: str):
    team_list = []
    tn_list = []
    req_body = json.loads(request.body)
    with open(team_path, "rb") as ap:
        while True:
            try:
                team_dict = pickle.load(ap)
                if team_dict["id"] == req_body["id"]:
                    users_list = req_body["users"]
                    # users_str = request.GET.dict()['users'].strip('[').strip(']').replace('"','')
                    # users_list = users_str.split(',')
                    team_dict["users"].extend(users_list)
                    # team_dict['users'] = users_list
                    team_dict["users"] = list(set(team_dict["users"]))
                    validate_user_ids(team_dict["users"])

                team_list.append(team_dict)
            except EOFError:
                break
            except ValidationError as e:
                return JsonResponse({"message": e.message, "status_code": 500})
    os.remove(team_path)
    repopulate_tn_path(tn_list)
    with open(team_path, "ab") as ap:
        for team in team_list:
            pickle.dump(team, ap)

    return JsonResponse({"message": "Users updated"})


# add users to team
@api_view(["DELETE"])
@csrf_exempt
def remove_users_from_team(request: str):
    team_list = []
    tn_list = []
    req_body = json.loads(request.body)
    with open(team_path, "rb") as ap:
        while True:
            try:
                team_dict = pickle.load(ap)
                if team_dict["id"] == req_body["id"]:
                    users_list = req_body["users"]
                    # users_list = request.GET.dict()['users'].strip('[').strip(']').strip('"').split(',')
                    for user in users_list:
                        team_dict["users"].remove(user)
                team_list.append(team_dict)
            except EOFError:
                break
    os.remove(team_path)
    repopulate_tn_path(tn_list)
    with open(team_path, "ab") as ap:
        for team in team_list:
            pickle.dump(team, ap)

    return JsonResponse({"message": "Users removed"})


# list users of a team
@api_view(["GET"])
@csrf_exempt
def list_team_users(request: str):
    users_list = []
    users = []
    req_body = json.loads(request.body)
    with open(team_path, "rb") as ap:
        while True:
            try:
                team_dict = pickle.load(ap)
                if team_dict["id"] == req_body["id"]:
                    users = team_dict["users"]
                    break
            except EOFError:
                break

    with open(db_path, "rb") as ap:
        while True:
            try:
                user_dict = pickle.load(ap)
                if user_dict["id"] in users:
                    user_dict.pop("description")
                    user_dict.pop("creation_time")
                    users_list.append(user_dict)
            except EOFError:
                break

    return JsonResponse(json.dumps(users_list), safe=False)
