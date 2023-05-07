# Organization_app

Organization app for making to do -lists and note lists to keep track of things.

User can
* create a new account, sign in and sign out
* create new lists, name them and remove them
* add tasks on lists, mark them as done and remove them
* remove all tasks in a list that are marked as done
* reset all tasks in a list as undone for the purpose of reusing a to do -list as a checklist
* add entrys on note lists
* view a list of all list names and open lists one at a time

## Instructions to test app locally
(this app is not available for testing in fly.io)

* Clone this repository to your computer and go to its root directory and use the following command:

```$ cd organization_app/```

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
