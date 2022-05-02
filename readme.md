# Marvel Core (Backend)

## Instructions for run proyect

Create venv:
- install venv:
`py -m pip install --user virtualenv` - windows
`python -m pip install --user virtualenv` - linux
- create venv:
`virtualenv -p python3 venv`
- active venv:
`venv\Scripts\activate` - windows
`source venv\Scripts\activate` - linux

Install requirements (with venv active):

### `pip install -r requirements.txt`

build container (only the first time and for each change):

### `docker build -t marvelcore .`

start container:
you can change port 3200(docker port) for another that you want,
and 3200(application port) port can be changed in app.py file

### `docker run -it -p 3200:3200 -d marvelcore`

## For tests

Is important that docker container is running for tests.

### `pytests tests/test_routes.py`

## Documentation:
Also, you can check the documentation in:
(http://localhost:3200/apidocs/)

## Important

It's necesary create `.env` document and paste the data from `.env.dev`. Remember that you have to fill variables with your data.

You can generate your `API_KEY` and `API_HASH` creating an marvel developer account in the follow link: (https://developer.marvel.com/)

For `MONGO_USER` and `MONGO_PWD` you have to create an account in mongo atlas in the follow link: (https://account.mongodb.com/account/login)

## Important For mongoDB

Remember that connection to db is actually mine, you have to change this conection in `src/commands/utils.py`

Actually mongo database (`marvel`) and collection (`users`) is hardcoded in `src/commands/utils.py` file, you can change these values but have to be named with the same name in mongodb.



