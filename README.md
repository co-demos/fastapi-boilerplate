A simple boilerplate of an API server, powered by **[FastAPI][fastapi]** framework with a **PostgreSQL** database. 

This work in progress is mainly the result of studying [tutorials][fastapi-tuto] from official documentation, the [amazing fullstack FastAPI-PostgreSQL boilerplate][fastapi-boilerplate], and this [youtube playlist][MK-Fast].

The current goal is to make it work with the following generic features, so it could be adapted for later purposes :

- [ ] **PostgreSQL** database for storing large volumes of data,  keeping track of relations, and making queries in a simple way (easier than MongoDB at least)  ;
- [ ] **Oauth2** authentication for securiity and users management ;
- [ ] **SocketIO** endpoints for collaborative work ;
- [ ] **Email notifications** for password changes ;
- [ ] **Static files** server for avatars and so...
- [x] **CORS** implementation, to serve as SAAS API server ;
- [ ] **Dockerisation**, for dev purposes...

---

# INSTALLATION

<!-- ## 1/ Virtual env python -->

<!-- ```shell
pip install virtualenv
virtualenv env
source venv/bin/activate
``` -->

## Dependencies - PostgreSQL

- ubuntu

```shell
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql -c "SELECT version();"
```

- mac OS


cf : https://gist.github.com/ibraheem4/ce5ccd3e4d7a65589ce84f2a3b7c23a3
cf : https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb

```shell
brew doctor
brew update
brew install postgres
brew services start postgresql
```
<!-- ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents -->


## Dependencies - Python

<!--
```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
``` -->

We use [`pipenv`][pipenv] as package manager :

```shell
pipenv install --system --dev
```

or

```shell
pipenv install --three python-dotenv fastapi uvicorn sqlalchemy  sqlalchemy-utils pydantic[email] psycopg2 alembic python-multipart python-jose[cryptography] passlib[bcrypt] aiofiles fastapi-socketio requests inflect shutil
```

To reead more on [why pipenv](https://realpython.com/pipenv-guide/)...

## Environment variables

### The .env file

The environment variables must be stored in the `.env` file at the root of the repo. It contains confidential values such as : postgres url with password, email smtp values, JWT secret keys... 

A template - `example.env` - is present at the root. You can copy-paste it and customize it wiith your own values.

```shell
# from repo root
cp example.env .env
```

### Create secure random keys

To generatte random secret keys you  can use `openssl` command line or - if you feel lazy - [password generator website](https://passwordsgenerator.net/).

```shell
openssl rand -hex 32
```

... and copy-paste the key as `JWT_SECRET_KEY` in `.env` file


---

# RUNNING APP

## Run app

```shell
alembic upgrade head && pipenv run uvicorn sql_app.main:app --reload
```

then open the  following url in your browser `http://localhost:8000/docs`

---

## Migrations 

```shell
alembic revision --autogenerate -m "<Migration message>"
alembic upgrade head
```

cf : https://alexvanzyl.com/posts/2020-05-24-fastapi-simple-application-structure-from-scratch-part-2/


[fastapi]:https://fastapi.tiangolo.com/
[fastapi-tuto]:https://fastapi.tiangolo.com/tutorial/
[fastapi-boilerplate]:https://github.com/tiangolo/full-stack-fastapi-postgresql
[MK-fast]:https://www.youtube.com/watch?v=HnJEiTx0feE&list=PL_9Bx_sxJkROtrlVTsGiuu-NtO_BmUfkB

[pipenv]:https://pipenv-fork.readthedocs.io/en/latest/basics.html
