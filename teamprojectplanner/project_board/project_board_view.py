import os, json
import pickle

# from django.forms import ValidationError
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from project_schema import (
    BoardSchema,
    TaskSchema,
)
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import pandas as pd
from .views import team_path, all_task_path, task_path, absolute_path, board_path


@api_view(["POST"])
@csrf_exempt
def create_board(request):
    """
    :param request: A json string with the board details.
    {
        "name" : "<board_name>",
        "description" : "<description>",
        "team_id" : "<team id>"
    }
    :return: A json string with the response {"id" : "<board_id>"}

    Constraint:
        * board name must be unique for a team
        * board name can be max 64 characters
        * description can be max 128 characters
    """
    try:
        data = BoardSchema().load(json.loads(request.body))
    except ValidationError as e:
        return JsonResponse({"message": e.message, "status_code": 500})
    with open(board_path, "ab") as ap:
        pickle.dump(data, ap)
    return JsonResponse({"id": data["id"]})


# close a board
@api_view(["POST"])
@csrf_exempt
def close_board(request) -> str:
    """
    :param request: A json string with the user details
    {
        "id" : "<board_id>"
    }

    :return:

    Constraint:
        * Set the board status to CLOSED and record the end_time date:time
        * You can only close boards with all tasks marked as COMPLETE
    """
    board_list = []
    req_body = json.loads(request.body)
    found = False
    with open(board_path, "rb") as ap:
        while True:
            try:
                board = pickle.load(ap)
                if board["id"] == req_body["id"]:
                    found = True
                    board["status"] = "CLOSED"
                board_list.append(board)
            except EOFError:
                if not found:
                    return JsonResponse({"message": "Board not found"})
                else:
                    break
    os.remove(board_path)
    with open(board_path, "ab") as ap:
        for board in board_list:
            pickle.dump(board, ap)

    return JsonResponse({"message": "Board closed."})


# add task to board
@api_view(["POST"])
@csrf_exempt
def add_task(request) -> str:
    """
    :param request: A json string with the task details. Task is assigned to a user_id who works on the task
    {
        "title" : "<board_name>",
        "description" : "<description>",
        "team_id" : "<team id>"
    }
    :return: A json string with the response {"id" : "<task_id>"}

    Constraint:
        * task title must be unique for a board
        * title name can be max 64 characters
        * description can be max 128 characters

    Constraints:
    * Can only add task to an OPEN board
    """
    try:
        req_body = json.loads(request.body)
        team_id = 0
        users = []
        if os.path.isfile(team_path):
            with open(team_path, "rb") as ap:
                while True:
                    try:
                        team = pickle.load(ap)
                        if req_body["user_id"] in team["users"]:
                            users = team["users"]
                            team_id = team["id"]
                    except EOFError:
                        break

        if os.path.isfile(board_path):
            with open(board_path, "rb") as ap:
                while True:
                    try:
                        board = pickle.load(ap)
                        if board["team_id"] == team_id:
                            if board["status"] == "CLOSED":
                                return JsonResponse({"message": "Board is closed."})
                    except EOFError:
                        break
        data = TaskSchema().load(json.loads(request.body))

        if os.path.isfile(task_path):
            with open(task_path, "rb") as ap:
                while True:
                    try:
                        user_task = pickle.load(ap)
                        if list(user_task.keys())[0] in users:
                            if data["title"] in list(user_task.values())[0]:
                                raise ValidationError("Title already present.")

                    except EOFError:
                        break
        with open(task_path, "ab") as ap:
            pickle.dump({data["user_id"]: [data["title"]]}, ap)
    except ValidationError as e:
        return JsonResponse({"message": e.message, "status_code": 500})
    with open(all_task_path, "ab") as ap:
        pickle.dump(data, ap)
    return JsonResponse({"id": data["id"]})


# update the status of a task
@api_view(["PATCH"])
@csrf_exempt
def update_task_status(request: str):
    """
    :param request: A json string with the user details
    {
        "id" : "<task_id>",
        "status" : "OPEN | IN_PROGRESS | COMPLETE"
    }
    """
    req_body = json.loads(request.body)
    task_list = []
    found = False
    with open(all_task_path, "rb") as ap:
        while True:
            try:
                task = pickle.load(ap)
                if task["id"] == req_body["id"]:
                    found = True
                    task["status"] = req_body["status"]
                task_list.append(task)
            except EOFError:
                if not found:
                    return JsonResponse({"message": "Task not found"})
                else:
                    break

    os.remove(all_task_path)

    with open(all_task_path, "ab") as ap:
        for task in task_list:
            pickle.dump(task, ap)

    return JsonResponse({})


# list all open boards for a team
@api_view(["GET"])
@csrf_exempt
def list_boards(request: str) -> str:
    """
    :param request: A json string with the team identifier
    {
        "id" : "<team_id>"
    }

    :return:
    [
        {
        "id" : "<board_id>",
        "name" : "<board_name>"
        }
    ]
    """
    board_list = []
    req_body = json.loads(request.body)
    with open(board_path, "rb") as ap:
        while True:
            try:
                board = pickle.load(ap)
                if board["team_id"] == req_body["id"]:
                    found = True
                    board.pop("creation_time")
                    board.pop("description")
                    board.pop("status")
                    board.pop("team_id")
                    board_list.append(board)

            except EOFError:
                if not found:
                    return JsonResponse({"message": "Team not found."})
                else:
                    break

    return JsonResponse(json.dumps(board_list), safe=False)


@api_view(["GET"])
@csrf_exempt
def export_board(request: str) -> str:
    """
    Export a board in the out folder. The output will be a txt file.
    We want you to be creative. Output a presentable view of the board and its tasks with the available data.
    :param request:
    {
        "id" : "<board_id>"
    }
    :return:
    {
        "out_file" : "<name of the file created>"
    }
    """
    req_body = json.loads(request.body)
    outfile_path = Path(absolute_path).parent.parent / f"out/board-{req_body['id']}.txt"
    found = False
    team_id = 0
    users = []
    task_list = []

    with open(board_path, "rb") as ap:
        while True:
            try:
                board = pickle.load(ap)
                if board["id"] == req_body["id"]:
                    found = True
                    team_id = board["team_id"]
                    break
            except EOFError:
                if not found:
                    return JsonResponse({"message": "Board not found."})
                else:
                    break

    with open(team_path, "rb") as ap:
        while True:
            try:
                team = pickle.load(ap)
                if team["id"] == team_id:
                    users = team["users"]
                    break
            except EOFError:
                break

    with open(all_task_path, "rb") as ap:
        while True:
            try:
                task = pickle.load(ap)
                if task["user_id"] in users:
                    task_list.append(task)
            except EOFError:
                break

    tasks_df = pd.DataFrame(task_list)
    with open(outfile_path, mode="w") as file_object:
        print(tasks_df, file=file_object)

    return JsonResponse(
        {"message": f"File exported. You can find the file at {outfile_path}"}
    )
