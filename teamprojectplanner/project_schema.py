import os
from pathlib import Path
from django.core.exceptions import ValidationError
from marshmallow import (
    EXCLUDE,
    Schema,
    fields,
    post_load,
    pre_dump,
    pre_load,
    validate,
    validates_schema,
)
import pickle
import uuid
from datetime import datetime


absolute_path = os.path.dirname(__file__)
uid_path = Path(absolute_path).parent / "db/userids.pickle"
un_path = Path(absolute_path).parent / "db/usernames.pickle"
team_path = Path(absolute_path).parent / "db/teamnames.pickle"
teamboard_path = Path(absolute_path).parent / "db/teamboard.pickle"


def repopulate_un_path(un_list):
    os.remove(un_path)
    with open(un_path, "ab") as ap:
        for un in un_list:
            pickle.dump(un, ap)


def repopulate_tn_path(tn_list):
    os.remove(team_path)
    with open(team_path, "ab") as ap:
        for tn in tn_list:
            pickle.dump(tn, ap)


def validate_unique_username(name: str):
    un_list = []
    if os.path.isfile(un_path):
        with open(un_path, "rb") as r:
            while True:
                try:
                    un_list.append(pickle.load(r))
                except EOFError:
                    break

    if name in un_list or len(name) > 64:
        raise ValidationError(
            "Username already present or length excees maximum allowed of 64 characters."
        )

    return name


class UserSchema(Schema):
    id = fields.String(required=True, load_only=True)
    name = fields.String(required=True, validate=validate_unique_username)
    display_name = fields.String(
        required=True, validate=validate.Length(max=64), load_only=True
    )
    creation_time = fields.DateTime(required=True)
    description = fields.String(required=True)

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def generate_fields(self, data, **kwargs):
        if not data.get("id"):
            data["id"] = str(uuid.uuid1())

        if not data.get("creation_time"):
            data["creation_time"] = datetime.now().isoformat()
        else:
            data["creation_time"] = data.get("creation_time").isoformat()

        if not data.get("description"):
            data["description"] = f"This is User, id - {data['id']}"
        return data

    @post_load
    def add_to_usernames_pickle(self, data, **kwargs):
        """
        adds usernames to a seperate pickle file so that we dont have to load them again.
        """
        with open(un_path, "ab") as ap:
            pickle.dump(data["name"], ap)

        with open(uid_path, "ab") as ap:
            pickle.dump(data["id"], ap)

        return data


def validate_unique_teamname(name: str):
    un_list = []
    if os.path.isfile(team_path):
        with open(team_path, "rb") as r:
            while True:
                try:
                    un_list.append(pickle.load(r))
                except EOFError:
                    break

    if name in un_list or len(name) > 64:
        print(name)
        print(un_list)
        raise ValidationError(
            "Teamname already present or length excees maximum allowed of 64 characters."
        )

    return name


def validate_user_ids(user_list: list):
    uid_list = []
    if os.path.isfile(uid_path):
        with open(uid_path, "rb") as r:
            while True:
                try:
                    uid_list.append(pickle.load(r))
                except EOFError:
                    break
        print(user_list)
        print(uid_list)
        for user in user_list:
            if user not in uid_list:
                raise ValidationError("UserId invalid.")

    if len(user_list) > 50:
        raise ValidationError("UserIds length exceeds maximum allowed of 50 items.")

    return user_list


def validate_admin_id(admin_id: str):
    uid_list = []
    if os.path.isfile(uid_path):
        with open(uid_path, "rb") as r:
            while True:
                try:
                    uid_list.append(pickle.load(r))
                except EOFError:
                    break
        if admin_id not in uid_list:
            raise ValidationError("Admin userId invalid.")

    return admin_id


class TeamSchema(Schema):
    id = fields.String(required=True, load_only=True)
    name = fields.String(required=True, validate=validate_unique_teamname)
    admin = fields.String(required=True, validate=validate_admin_id)
    creation_time = fields.DateTime(required=True)
    description = fields.String(required=True, validate=validate.Length(max=128))
    users = fields.List(
        fields.Str(), required=False, load_default=[], validate=validate_user_ids
    )

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def generate_fields(self, data, **kwargs):
        if not data.get("id"):
            data["id"] = str(uuid.uuid1())
        if not data.get("creation_time"):
            data["creation_time"] = datetime.now().isoformat()
        else:
            data["creation_time"] = data.get("creation_time").isoformat()
        data["users"] = [data["admin"]]
        return data

    @post_load
    def add_to_teamnames_pickle(self, data, **kwargs):
        """
        adds usernames to a seperate pickle file so that we dont have to load them again.
        """
        with open(team_path, "ab") as ap:
            pickle.dump(data["name"], ap)

        return data

    @pre_dump
    def fix_datetime(self, data, **kwargs):
        pass


class BoardSchema(Schema):
    id = fields.String(required=True, load_only=True)
    name = fields.String(required=True, validate=validate.Length(max=64))
    creation_time = fields.DateTime(required=True)
    description = fields.String(required=True, validate=validate.Length(max=128))
    team_id = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(("OPEN", "CLOSED")))

    @validates_schema(skip_on_field_errors=True)
    def validate_unique_boardname(self, data, **kwargs):
        teamboard_list = []
        if os.path.isfile(teamboard_path):
            with open(teamboard_path, "rb") as r:
                while True:
                    try:
                        teamboard = pickle.load(r)
                        if list(teamboard.keys())[0] == data["team_id"]:
                            if data["name"] in teamboard[data["team_id"]]:
                                raise ValidationError("Board name already present.")
                    except EOFError:
                        break

    @pre_load
    def generate_fields(self, data, **kwargs):
        if not data.get("id"):
            data["id"] = str(uuid.uuid1())
        if not data.get("creation_time"):
            data["creation_time"] = datetime.now().isoformat()
        else:
            data["creation_time"] = data.get("creation_time").isoformat()
        data["status"] = "OPEN"
        return data

    @post_load
    def add_to_teamboard_pickle(self, data, **kwargs):
        """
        adds usernames to a seperate pickle file so that we dont have to load them again.
        """
        teamboard_list = []
        found = False
        if os.path.isfile(teamboard_path):
            with open(teamboard_path, "rb") as ap:
                while True:
                    try:
                        team_board = pickle.load(ap)
                        if list(team_board.keys())[0] == data["team_id"]:
                            if data["name"] in team_board[data["team_id"]]:
                                team_board[data["team_id"]].append(data["name"])
                                found = True
                        teamboard_list.append(team_board)
                    except EOFError:
                        break

        if found:
            os.remove(teamboard_path)
            with open(teamboard_path, "ab") as ap:
                for teamboard in teamboard_list:
                    pickle.dump(teamboard, ap)
        else:
            with open(teamboard_path, "ab") as ap:
                teamboard = {data["team_id"]: [data["name"]]}
                pickle.dump(teamboard, ap)
        return data


def validate_user_id(user_id: int):
    return validate_user_ids([user_id])[0]


class TaskSchema(Schema):
    id = fields.String(required=True, load_only=True)
    title = fields.String(required=True, validate=validate.Length(max=64))
    creation_time = fields.DateTime(required=True)
    description = fields.String(required=True, validate=validate.Length(max=128))
    user_id = fields.Str(required=True, validate=validate_user_id)
    status = fields.Str(
        required=True, validate=validate.OneOf(("OPEN", "IN_PROGRESS", "COMPLETE"))
    )

    @validates_schema(skip_on_field_errors=True)
    def validate_unique_taskname(self, data, **kwargs):
        teamboard_list = []
        if os.path.isfile(teamboard_path):
            with open(teamboard_path, "rb") as r:
                while True:
                    try:
                        teamboard = pickle.load(r)
                        if list(teamboard.keys())[0] == data["user_id"]:
                            if data["title"] in teamboard[data["user_id"]]:
                                raise ValidationError("Task name already present.")
                    except EOFError:
                        break

    @pre_load
    def generate_fields(self, data, **kwargs):
        if not data.get("id"):
            data["id"] = str(uuid.uuid1())
        if not data.get("creation_time"):
            data["creation_time"] = datetime.now().isoformat()
        else:
            data["creation_time"] = data.get("creation_time").isoformat()
        data["status"] = "OPEN"
        return data

    @post_load
    def add_to_teamboard_pickle(self, data, **kwargs):
        """
        adds usernames to a seperate pickle file so that we dont have to load them again.
        """
        teamboard_list = []
        found = False
        if os.path.isfile(teamboard_path):
            with open(teamboard_path, "rb") as ap:
                while True:
                    try:
                        team_board = pickle.load(ap)
                        if list(team_board.keys())[0] == data["user_id"]:
                            if data["title"] in team_board[data["user_id"]]:
                                team_board[data["user_id"]].append(data["title"])
                                found = True
                        teamboard_list.append(pickle.load(ap))
                    except EOFError:
                        break

        if found:
            os.remove(teamboard_path)
            with open(teamboard_path, "ab") as ap:
                for teamboard in teamboard_list:
                    pickle.dump(teamboard, ap)
        else:
            with open(teamboard_path, "ab") as ap:
                teamboard = {data["user_id"]: [data["title"]]}
                pickle.dump(teamboard, ap)
        return data
