# Getting Started
- Clone repository (You are here!)
- create venv and launch venv
  - run `python -m venv new_env`
  - run `source new_env/bin/activate`
- Load libraries
  - run `pip install -r requirements.txt`

# Setting up database
- run `./manage.py migrate` to create the database and schema
  - If changes are made to models.py then `./manage.py makemigration` and `./manage.py migrate` will need to be run

# Bootstrapping users and data
- run `./manage.py bootstrap` to load data and set up users
  - Records in data/leagues.csv and data/teams.csv are loaded into the database
  - Users _admin_ and _commish_ are created
    - Password for both is `123123`
- Users can be reloaded by supplying `--users` parameter: `./manage.py bootstrap --users`. This command is idempotent.
- Data can be loaded by supplying `--db` parameter: `./manage.py bootstrap --db`
  -  Note that loading data is not idempotent. If this is run when data is already in the database an error will occur.

# Start the application
- run `./manage.py runserver`
- go to application's URL: http://127.0.0.1:8000/

# Cleanup
- Run `./manage.py flush` to clear all the data
- Run bootstrap again to replace the data


