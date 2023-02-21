import os
from pathlib import Path

absolute_path = os.path.dirname(__file__)
db_path = Path(absolute_path).parent.parent / "db/users.pickle"
board_path = Path(absolute_path).parent.parent / "db/boards.pickle"
team_path = Path(absolute_path).parent.parent / "db/teams.pickle"
task_path = Path(absolute_path).parent.parent / "db/tasks.pickle"
all_task_path = Path(absolute_path).parent.parent / "db/alltasks.pickle"
