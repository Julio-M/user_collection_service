[![CI](https://github.com/Julio-M/user_collection_service/actions/workflows/workflow.yml/badge.svg)](https://github.com/Julio-M/user_collection_service/actions/workflows/workflow.yml)

## myHome

### Introduction

This repository contains all the code for myHome backend services.
This repository is single source of truth for

- All Backend Microservices code `(./services/)`

## How to

### How to run the code locally ?

This will create a venv, install all the dependencied and start the server

```shell script
make run module=authentication
```

### How to make migrations ?

```shell script
make migrations name=<nameyourmigration>
```

```shell script
make migrate
```

### How to cleanup the enviroment ?

This will delete the venv, migrations files and the temporary database

```shell script
make cleanup
```

### I want to run test cases for a service?

```shell script
make test module=authentication
```

### Repository structure (Temp)

```shell script
.
├── Makefile
├── README.md
├── deploy.sh
└── services
    ├── __init__.py
    ├── alembic
    │   ├── README
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions
    ├── alembic.ini
    └── authentication
        ├── __init__.py
        ├── api
        │   ├── __init__.py
        │   ├── api_v1
        │   │   ├── __init__.py
        │   │   ├── api.py
        │   │   └── endpoints
        │   │       ├── __init__.py
        │   │       ├── login.py
        │   │       └── signup.py
        │   └── deps.py
        ├── core
        │   ├── config.py
        │   └── hashing.py
        ├── crud
        │   └── user_crud.py
        ├── db
        │   ├── __initi__.py
        │   ├── base_class.py
        │   └── session.py
        ├── main.py
        ├── models
        │   ├── __init__.py
        │   └── user_model.py
        ├── requirements.txt
        ├── schemas
        │   ├── token_schema.py
        │   └── user_schema.py
        ├── tests
        └── utils.py
```

**./services/**: Independent python modules for each service.
