# No DB Taskboard
## _The Best Taskboard ever_

No DB Taskboard is a taskboard that you can use to create boards, tasks, teams and users.
You can use the taskboard to track your tasks, their status and prepare boards.

## Installation
- Clone the repo
- Install requirements
    ```sh
    pip install -r requirements.txt
    ```
- Change to project directory
    ```
    cd teamprojectplanner
    ```
- Start the server
    ```sh
    python manage.py runserver 8003
    ```
    this will start the server on localhost:8003

## Development assumptions
- A team can be seen on multiple boards but a board can only be linked to 1 team.

## Development methodology

I have used pickling to persist data in file i.e. system memory as that would be the most effective to store and load back again, as we would have to load it everytime to compare.

There is 1 pickle file for each - tasks, teams, boards, users. In addition there is a pickle file for certain field that we need for validation as well like - teamboards, teamnames, userid, usernames.

I am using marshmallow for serialisation and validation of data. I have used @pre_load decorators provided by marshmallow to auto-generate the fields not provided and @post_load decorators to add intermediate data like user_id, username, teamboard mapping to pickle files. ValidationError is returned as Response when occurred.

I have use context manager everytime when dealing with pickle files so as to close file IO sessions.

We are also repopulating pickle files and intermediary files after updation so as not to have stale data.