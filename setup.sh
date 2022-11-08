#!/bin/bash

set -e
# set -e causes the shell to exit if any subcommand or pipeline returns a non-zero status.

######### CONSTANTS #############################
export TERM=xterm-256color
export BASE_DIR=$(pwd)
######### CONSTANTS #############################

function health() {
    echo "I am reachable"
    echo "$(whoami)"
}

function activateEnv(){
    N=1
    if [ "$#" -ne ${N} ]; then
        echo "activateVenv needs ${N} parameter(s)"
        exit 1
    fi
    moduleName=$1
    VENV_NAME="env-${moduleName}"
    echo "--> Checking for virutalenviroment <-----"
    if [[ -e "${VENV_NAME}" ]]; then
        echo "---Enviroment exists---"
    else
        echo ">-Creating new enviroment-<"
        python3 -m venv "${VENV_NAME}"
        echo ">-Done-<"
    fi
    VENV_DIR="${BASE_DIR}/${VENV_NAME}"
    VENV_EXECUTABLE="${VENV_DIR}/bin/activate"
    moduleBasePath="./services/${moduleName}"
    echo "--> Activating virutalenviroment ${VENV_NAME}<-----"
    source "${VENV_EXECUTABLE}"
    pip install -U pip &&
    echo "Using $(which python)" &&
    pip install -r "${moduleBasePath}"/requirements.txt &&
    pip install uvicorn==0.17.6
}


function runLocally() {
    # Variables needed for executing apps locally
    export DB_URI="postgresql://$(whoami):$(whoami)@localhost:5432/usersdb?connect_timeout=10"
    # export DB_URI="sqlite:///database.db"
    export SECRET_KEY="secret"
    export REFRESH_TOKEN="secret2"
    export PYTHONPATH="$(pwd)/services/${moduleName}"
    N=1
    if [ "$#" -ne ${N} ]; then
        echo "runModule needs ${N} parameter(s)"
        exit 1
    fi
    
    moduleName=$1
    executablePath="main:app"
    
    activateEnv "${moduleName}" &&
    clear &&
    cd ./services/"${moduleName}" &&
    uvicorn --host=0.0.0.0 --port=9558 --workers=1 --limit-concurrency=50 \
    --backlog=100 --use-colors \
    "${executablePath}" --reload
}

function deleteEnv(){
    N=1
    if [ "$#" -ne ${N} ]; then
        echo "delete_venv needs ${N} parameter(s)"
        exit 1
    fi
    moduleName=$1
    VENV_NAME="env-${moduleName}"
    echo "--> Deleting Virtual Environment <-----"
    echo "--> Checking for virutalenviroment <-----"
    if [[ -e "${VENV_NAME}" ]]; then
        echo "---Enviroment found---"
        echo "---Deleting---"
        rm -rf "${VENV_NAME}"
    else
        echo "---No venv set---"
    fi
}

function cleanup(){
    N=1
    if [ "$#" -ne ${N} ]; then
        echo "cleanup needs ${N} parameter(s)"
        exit 1
    fi
    moduleName=$1
    rm -rf services/__pycache__
    rm -rf services/alembic/__pycache__
    rm -rf services/alembic/versions/__pycache__
    rm -rf services/alembic/versions/*.py
    deleteEnv "${moduleName}"
}

function makeMigrations() {
      # Variables needed for executing apps locally
    export DB_URI="postgresql://$(whoami):$(whoami)@localhost:5432/usersdb?connect_timeout=10"
    # export DB_URI="sqlite:///database.db"
    export SECRET_KEY="secret"
    export REFRESH_TOKEN="secret2"
    export PYTHONPATH="$(pwd)/services/authentication"
    N=1
    if [ "$#" -ne ${N} ]; then
        echo "makeMigrations needs ${N} parameter(s)"
        exit 1
    fi
    cd ./services/
    migrationName=$1
    echo "--> Making migrations <-----"
    alembic revision --autogenerate -m "${migrationName}"
    echo "--> Done <-----"
}

function migrate(){
    # Variables needed for executing apps locally
    export DB_URI="postgresql://$(whoami):$(whoami)@localhost:5432/usersdb?connect_timeout=10"
    # export DB_URI="sqlite:///database.db"
    export SECRET_KEY="secret"
    export REFRESH_TOKEN="secret2"
    export PYTHONPATH="$(pwd)/services/authentication"
    echo "--> Migrate <-----"
    cd ./services/
    alembic upgrade head
    echo "--> Done <-----"
}

function test(){
    N=1
    if [ "$#" -ne ${N} ]; then
        echo "delete_venv needs ${N} parameter(s)"
        exit 1
    fi
    moduleName=$1
    export DB_URI="postgresql://$(whoami):$(whoami)@localhost:5432/usersdb?connect_timeout=10"
    # export DB_URI="sqlite:///database.db"
    export SECRET_KEY="secret"
    export REFRESH_TOKEN="secret2"
    export PYTHONPATH="$(pwd)/services/${moduleName}"
    activateEnv "${moduleName}" &&
    pytest -rf -v -p no:warnings \
    --disable-pytest-warnings ./services/${moduleName}/tests &&
    pylint --disable=R,C services/
}