# Marvel Core (Backend)

## Instructions for run proyect

build container (only the first time and for each change):

### `docker build -t marvelcore .`

start container:
you can change port 7000(docker port) for another that you want,
and 3200(application port) port can be changed in app.py file

### `docker run -it -p 7000:3200 -d marvelcore`

## Important

It's necesary create `.env` document and paste the data from `.env.dev`. Remember that you have to fill variables with your data.

You can generate your `API_KEY` and `API_HASH` creating an marvel developer account in the follow link: (https://developer.marvel.com/)

For `MONGO_USER` and `MONGO_PWD` you have to create an account in mongo atlas in the follow link: (https://account.mongodb.com/account/login)

## Important For mongoDB

Actually mongo database (`marvel`) and collection (`users`) is hardcoded in `src/commands/utils.py` file, you can change these values but have to be named with the same name in mongodb.


## For create venv
Install venv:
`py -m pip install --user virtualenv`
Create venv:
`virtualenv -p python3 venv`
Active venv:
`venv\Scripts\activate`
