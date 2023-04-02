# Organization_app

Organization app for making to do lists, note lists and reusable checklists.

User can
* create a new account, sign in and sign out
* create new lists, name them and remove them
* add tasks on lists, mark them as done and remove them
* add notes/entrys on lists and remove them
* remove all tasks in a list that are marked as done
* reset all tasks in a list as undone for the purpose of reusing a checklist
* view a list of all list names and open lists one at a time
* view the amount of done and undone tasks in a list
* mark a task as a high priority task
* view all high priority tasks from all lists in the high priority section 

## Current version of the app

In current version of the app:

User can
* create a new account, sign in and sign out
* create new lists and name them
* add tasks on lists mark them as done and as undone
* view a list of all lists and open lists one at a time


## Instructions to test app locally

* Clone this repository to your computer and go to its root directory.
* Create file .env and set its contents as follows:

```DATABASE_URL=<database-local-address>```

```SECRET_KEY=<secret-key>```

* Activate virtual environment and install app dependencies with following commands:

```$ python3 -m venv venv```

```$ source venv/bin/activate```

```$ pip install -r ./requirements.txt```

* Set database scheme with command:

```$ psql < schema.sql```

* Run application with command:

```$ flask run```