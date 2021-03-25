# INSTALLATION

<!-- ## 1/ Virtual env python -->

<!-- ```shell
pip install virtualenv
virtualenv env
source venv/bin/activate
``` -->

## Install postgresql

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


## Dependencies

<!-- ```shell
python -m pip install --upgrade pip
pip install python-dotenv
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install psycopg2
pip install python-multipart
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install aiofiles
pip install fastapi-socketio
```

or 

```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
``` -->

We use `pipenv` as package manager :

```shell
pipenv install --system --dev
```

or

```shell
pipenv install --three python-dotenv fastapi uvicorn sqlalchemy  sqlalchemy-utils pydantic[email] psycopg2 alembic python-multipart python-jose[cryptography] passlib[bcrypt] aiofiles fastapi-socketio requests inflect
```

## Create secure random key

```shell
openssl rand -hex 32
```

and copy-paste the key as `JWT_SECRET_KEY` in `.env` file


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
