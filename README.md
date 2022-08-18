## myHome

### Introduction

This repository contains all the code for myHome backend services.
This repository is single source of truth for

- All Backend Microservices code `(./services/)`

## How to

### How to run the code locally ?

```shell script
make run module=authentication
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
    ├── authentication
    │   ├── __init__.py
    │   ├── core
    │   │   ├── models
    │   │   │   └── __init__.py
    │   │   ├── schemas
    │   │   │   └── __init__.py
    │   │   └── settings.py
    │   ├── main.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   └── v1
    │   │       └── __init__.py
    │   └── v1
    │       ├── __init__.py
    │       └── endpoints
    │           └── __init__.py
    └── authorizer
```

**./services/**: Independent python modules for each service.
