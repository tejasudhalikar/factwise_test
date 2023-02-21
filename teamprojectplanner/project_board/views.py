import os
from pathlib import Path

absolute_path = os.path.dirname(__file__)
db_path = Path(absolute_path).parent.parent / "db/users.pickle"
board_path = Path(absolute_path).parent.parent / "db/boards.pickle"
team_path = Path(absolute_path).parent.parent / "db/teams.pickle"
task_path = Path(absolute_path).parent.parent / "db/tasks.pickle"
all_task_path = Path(absolute_path).parent.parent / "db/alltasks.pickle"

# Create your views here.
# @api_view(["POST"])
# @csrf_exempt
# def create_user(request) -> str:
#     req_body = json.loads(request.body)
#     try:
#         data = UserSchema().load(req_body)
#     except ValidationError as e:
#         return JsonResponse({"message": e.message, "status_code": 500})
#     with open(db_path, "ab") as ap:
#         pickle.dump(data, ap)
#     return JsonResponse({"id": data["id"]})


# @api_view(["GET"])
# @csrf_exempt
# def list_users(request) -> str:
#     user_list = []
#     with open(db_path, "rb") as ap:
#         while True:
#             try:
#                 user_list.append(UserSchema().dump(pickle.load(ap)))
#             except EOFError:
#                 break
#     return JsonResponse(json.dumps(user_list), safe=False)


# @api_view(["GET"])
# @csrf_exempt
# def describe_user(request) -> str:
#     user_dict = {}
#     req_body = json.loads(request.body)
#     with open(db_path, "rb") as ap:
#         while True:
#             try:
#                 user_dict = pickle.load(ap)
#                 if user_dict["id"] == req_body["id"]:
#                     user_dict.pop("id")
#                     user_dict.pop("display_name")
#                     break
#                 else:
#                     user_dict = {}
#             except EOFError:
#                 break

#     if not user_dict:
#         return JsonResponse({"message": "User Not Found", "status_code": 404})

#     return JsonResponse(user_dict)


# @api_view(["PATCH"])
# @csrf_exempt
# def update_user(request) -> str:
#     user_list = []
#     un_list = []
#     req_body = json.loads(request.body)
#     with open(db_path, "rb") as ap:
#         while True:
#             try:
#                 user_dict = pickle.load(ap)
#                 if user_dict["id"] == req_body["id"]:
#                     user_det = json.loads(req_body["user"])
#                     user_dict["name"] = user_det["name"]
#                     user_dict["display_name"] = user_det["display_name"]
#                 data = TeamSchema().load(user_dict)
#                 un_list.append(user_dict["name"])
#                 user_list.append(data)
#             except EOFError:
#                 break
#             except ValidationError as e:
#                 return JsonResponse({"message": e.message, "status_code": 500})

#     os.remove(db_path)

#     # repopulates usernames pickle
#     repopulate_un_path(un_list)
#     with open(db_path, "ab") as ap:
#         for user in user_list:
#             pickle.dump(user, ap)

#     return JsonResponse({"message": "User updated"})


# @api_view(["GET"])
# @csrf_exempt
# def get_user_teams(request):
#     teams_list = []
#     req_body = json.loads(request.body)
#     with open(team_path, "rb") as ap:
#         while True:
#             try:
#                 team_dict = pickle.load(ap)
#                 if req_body["id"] in team_dict["users"]:
#                     team_dict.pop("id")
#                     team_dict.pop("users")
#                     team_dict["creation_time"] = str(team_dict["creation_time"])
#                     teams_list.append(team_dict)
#             except EOFError:
#                 break

#     return JsonResponse(json.dumps(teams_list), safe=False)


# @api_view(["POST"])
# @csrf_exempt
# def create_team(request) -> str:
#     req_body = json.loads(request.body)
#     try:
#         data = TeamSchema().load(req_body)
#     except ValidationError as e:
#         return JsonResponse({"message": e.message, "status_code": 500})
#     with open(team_path, "ab") as ap:
#         pickle.dump(data, ap)
#     return JsonResponse({"id": data["id"]})


# @api_view(["GET"])
# @csrf_exempt
# def list_teams(request) -> str:
#     team_list = []
#     with open(team_path, "rb") as ap:
#         while True:
#             try:
#                 team = pickle.load(ap)
#                 team.pop("id")
#                 team.pop("users")
#                 team["creation_time"] = str(team["creation_time"])
#                 team_list.append(team)
#             except EOFError:
#                 break
#     return JsonResponse(json.dumps(team_list), safe=False)


# @api_view(["GET"])
# @csrf_exempt
# def describe_team(request) -> str:
#     team_dict = {}
#     req_body = json.loads(request.body)
#     with open(team_path, "rb") as ap:
#         while True:
#             try:
#                 team_dict = pickle.load(ap)
#                 if team_dict["id"] == req_body["id"]:
#                     team_dict.pop("id")
#                     break
#                 else:
#                     team_dict = {}
#             except EOFError:
#                 break

#     if not team_dict:
#         return JsonResponse({"message": "Team Not Found", "status_code": 404})

#     return JsonResponse(team_dict)


# @api_view(["PATCH"])
# @csrf_exempt
# def update_team(request) -> str:
#     team_list = []
#     tn_list = []
#     req_body = json.loads(request.body)
#     with open(team_path, "rb") as ap:
#         while True:
#             try:
#                 team_dict = pickle.load(ap)
#                 if team_dict["id"] == req_body["id"]:
#                     team_det = req_body["team"]
#                     team_dict["name"] = team_det["name"]
#                     team_dict["description"] = team_det["description"]
#                     team_dict["admin"] = team_det["admin"]
#                     data = TeamSchema().load(team_dict)
#                 tn_list.append(team_dict["name"])
#                 team_list.append(team_dict)
#             except EOFError:
#                 break
#             except ValidationError as e:
#                 return JsonResponse({"message": e.message, "status_code": 500})
#     os.remove(team_path)
#     repopulate_tn_path(tn_list)
#     with open(team_path, "ab") as ap:
#         for team in team_list:
#             pickle.dump(team, ap)

#     return JsonResponse({"message": "Team updated"})


# @api_view(["PATCH"])
# @csrf_exempt
# def add_users_to_team(request: str):
#     team_list = []
#     tn_list = []
#     req_body = json.loads(request.body)
#     with open(team_path, "rb") as ap:
#         while True:
#             try:
#                 team_dict = pickle.load(ap)
#                 if team_dict["id"] == req_body["id"]:
#                     users_list = req_body["users"]
#                     # users_str = request.GET.dict()['users'].strip('[').strip(']').replace('"','')
#                     # users_list = users_str.split(',')
#                     team_dict["users"].extend(users_list)
#                     # team_dict['users'] = users_list
#                     team_dict["users"] = list(set(team_dict["users"]))
#                     validate_user_ids(team_dict["users"])

#                 team_list.append(team_dict)
#             except EOFError:
#                 break
#             except ValidationError as e:
#                 return JsonResponse({"message": e.message, "status_code": 500})
#     os.remove(team_path)
#     repopulate_tn_path(tn_list)
#     with open(team_path, "ab") as ap:
#         for team in team_list:
#             pickle.dump(team, ap)

#     return JsonResponse({"message": "Users updated"})


# # add users to team
# @api_view(["DELETE"])
# @csrf_exempt
# def remove_users_from_team(request: str):
#     team_list = []
#     tn_list = []
#     req_body = json.loads(request.body)
#     with open(team_path, "rb") as ap:
#         while True:
#             try:
#                 team_dict = pickle.load(ap)
#                 if team_dict["id"] == req_body["id"]:
#                     users_list = req_body["users"]
#                     # users_list = request.GET.dict()['users'].strip('[').strip(']').strip('"').split(',')
#                     for user in users_list:
#                         team_dict["users"].remove(user)
#                 team_list.append(team_dict)
#             except EOFError:
#                 break
#     os.remove(team_path)
#     repopulate_tn_path(tn_list)
#     with open(team_path, "ab") as ap:
#         for team in team_list:
#             pickle.dump(team, ap)

#     return JsonResponse({"message": "Users removed"})


# # list users of a team
# @api_view(["GET"])
# @csrf_exempt
# def list_team_users(request: str):
#     users_list = []
#     users = []
#     req_body = json.loads(request.body)
#     with open(team_path, "rb") as ap:
#         while True:
#             try:
#                 team_dict = pickle.load(ap)
#                 if team_dict["id"] == req_body["id"]:
#                     users = team_dict["users"]
#                     break
#             except EOFError:
#                 break

#     with open(db_path, "rb") as ap:
#         while True:
#             try:
#                 user_dict = pickle.load(ap)
#                 if user_dict["id"] in users:
#                     user_dict.pop("description")
#                     user_dict.pop("creation_time")
#                     users_list.append(user_dict)
#             except EOFError:
#                 break

#     return JsonResponse(json.dumps(users_list), safe=False)


# @api_view(["POST"])
# @csrf_exempt
# def create_board(request):
#     """
#     :param request: A json string with the board details.
#     {
#         "name" : "<board_name>",
#         "description" : "<description>",
#         "team_id" : "<team id>"
#     }
#     :return: A json string with the response {"id" : "<board_id>"}

#     Constraint:
#         * board name must be unique for a team
#         * board name can be max 64 characters
#         * description can be max 128 characters
#     """
#     try:
#         data = BoardSchema().load(json.loads(request.body))
#     except ValidationError as e:
#         return JsonResponse({"message": e.message, "status_code": 500})
#     with open(board_path, "ab") as ap:
#         pickle.dump(data, ap)
#     return JsonResponse({"id": data["id"]})


# # close a board
# @api_view(["POST"])
# @csrf_exempt
# def close_board(request) -> str:
#     """
#     :param request: A json string with the user details
#     {
#         "id" : "<board_id>"
#     }

#     :return:

#     Constraint:
#         * Set the board status to CLOSED and record the end_time date:time
#         * You can only close boards with all tasks marked as COMPLETE
#     """
#     board_list = []
#     req_body = json.loads(request.body)
#     found = False
#     with open(board_path, "rb") as ap:
#         while True:
#             try:
#                 board = pickle.load(ap)
#                 if board["id"] == req_body["id"]:
#                     found = True
#                     board["status"] = "CLOSED"
#                 board_list.append(board)
#             except EOFError:
#                 if not found:
#                     return JsonResponse({"message": "Board not found"})
#                 else:
#                     break
#     os.remove(board_path)
#     with open(board_path, "ab") as ap:
#         for board in board_list:
#             pickle.dump(board, ap)

#     return JsonResponse({"message": "Board closed."})


# # add task to board
# @api_view(["POST"])
# @csrf_exempt
# def add_task(request) -> str:
#     """
#     :param request: A json string with the task details. Task is assigned to a user_id who works on the task
#     {
#         "title" : "<board_name>",
#         "description" : "<description>",
#         "team_id" : "<team id>"
#     }
#     :return: A json string with the response {"id" : "<task_id>"}

#     Constraint:
#         * task title must be unique for a board
#         * title name can be max 64 characters
#         * description can be max 128 characters

#     Constraints:
#     * Can only add task to an OPEN board
#     """
#     try:
#         req_body = json.loads(request.body)
#         team_id = 0
#         users = []
#         if os.path.isfile(team_path):
#             with open(team_path, "rb") as ap:
#                 while True:
#                     try:
#                         team = pickle.load(ap)
#                         if req_body["user_id"] in team["users"]:
#                             users = team["users"]
#                             team_id = team["id"]
#                     except EOFError:
#                         break

#         if os.path.isfile(board_path):
#             with open(board_path, "rb") as ap:
#                 while True:
#                     try:
#                         board = pickle.load(ap)
#                         if board["team_id"] == team_id:
#                             if board["status"] == "CLOSED":
#                                 return JsonResponse({"message": "Board is closed."})
#                     except EOFError:
#                         break
#         data = TaskSchema().load(json.loads(request.body))

#         if os.path.isfile(task_path):
#             with open(task_path, "rb") as ap:
#                 while True:
#                     try:
#                         user_task = pickle.load(ap)
#                         if list(user_task.keys())[0] in users:
#                             if data["title"] in list(user_task.values())[0]:
#                                 raise ValidationError("Title already present.")

#                     except EOFError:
#                         break
#         with open(task_path, "ab") as ap:
#             pickle.dump({data["user_id"]: [data["title"]]}, ap)
#     except ValidationError as e:
#         return JsonResponse({"message": e.message, "status_code": 500})
#     with open(all_task_path, "ab") as ap:
#         pickle.dump(data, ap)
#     return JsonResponse({"id": data["id"]})


# # update the status of a task
# @api_view(["PATCH"])
# @csrf_exempt
# def update_task_status(request: str):
#     """
#     :param request: A json string with the user details
#     {
#         "id" : "<task_id>",
#         "status" : "OPEN | IN_PROGRESS | COMPLETE"
#     }
#     """
#     req_body = json.loads(request.body)
#     task_list = []
#     found = False
#     with open(all_task_path, "rb") as ap:
#         while True:
#             try:
#                 task = pickle.load(ap)
#                 if task["id"] == req_body["id"]:
#                     found = True
#                     task["status"] = req_body["status"]
#                 task_list.append(task)
#             except EOFError:
#                 if not found:
#                     return JsonResponse({"message": "Task not found"})
#                 else:
#                     break

#     os.remove(all_task_path)

#     with open(all_task_path, "ab") as ap:
#         for task in task_list:
#             pickle.dump(task, ap)

#     return JsonResponse({})


# # list all open boards for a team
# @api_view(["GET"])
# @csrf_exempt
# def list_boards(request: str) -> str:
#     """
#     :param request: A json string with the team identifier
#     {
#         "id" : "<team_id>"
#     }

#     :return:
#     [
#         {
#         "id" : "<board_id>",
#         "name" : "<board_name>"
#         }
#     ]
#     """
#     board_list = []
#     req_body = json.loads(request.body)
#     with open(board_path, "rb") as ap:
#         while True:
#             try:
#                 board = pickle.load(ap)
#                 if board["team_id"] == req_body["id"]:
#                     found = True
#                     board.pop("creation_time")
#                     board.pop("description")
#                     board.pop("status")
#                     board.pop("team_id")
#                     board_list.append(board)

#             except EOFError:
#                 if not found:
#                     return JsonResponse({"message": "Team not found."})
#                 else:
#                     break

#     return JsonResponse(json.dumps(board_list), safe=False)


# @api_view(["GET"])
# @csrf_exempt
# def export_board(request: str) -> str:
#     """
#     Export a board in the out folder. The output will be a txt file.
#     We want you to be creative. Output a presentable view of the board and its tasks with the available data.
#     :param request:
#     {
#         "id" : "<board_id>"
#     }
#     :return:
#     {
#         "out_file" : "<name of the file created>"
#     }
#     """
#     req_body = json.loads(request.body)
#     outfile_path = Path(absolute_path).parent.parent / f"out/board-{req_body['id']}.txt"
#     found = False
#     team_id = 0
#     users = []
#     task_list = []

#     with open(board_path, "rb") as ap:
#         while True:
#             try:
#                 board = pickle.load(ap)
#                 if board["id"] == req_body["id"]:
#                     found = True
#                     team_id = board["team_id"]
#                     break
#             except EOFError:
#                 if not found:
#                     return JsonResponse({"message": "Board not found."})
#                 else:
#                     break

#     with open(team_path, "rb") as ap:
#         while True:
#             try:
#                 team = pickle.load(ap)
#                 if team["id"] == team_id:
#                     users = team["users"]
#                     break
#             except EOFError:
#                 break

#     with open(all_task_path, "rb") as ap:
#         while True:
#             try:
#                 task = pickle.load(ap)
#                 if task["user_id"] in users:
#                     task_list.append(task)
#             except EOFError:
#                 break

#     tasks_df = pd.DataFrame(task_list)
#     with open(outfile_path, mode="w") as file_object:
#         print(tasks_df, file=file_object)

#     return JsonResponse(
#         {"message": f"File exported. You can find the file at {outfile_path}"}
#     )
