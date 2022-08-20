#!/bin/bash

set -e

ccend=$(tput sgr0)
ccso=$(tput smso)

######### CONSTANTS #############################

export PY_VERSION=3.9.0
export PYENV_ROOT=$(pyenv root)/
# export TEMPLATE_FILE_NAME="TBD"
export BASE_DIR=$(pwd)
# export LAMBDA_S3_BUCKET_NAME="TBD"
# export SAM_TEMPLATE_FILE_NAME="TBD"
# export CF_STACK_NAME="user-collection-service"

######### CONSTANTS #############################

function health() {
  echo "I am reachable"
}

function setupEnvironment() {
  echo "${ccso}--> Installing all the dependency <-----${ccend}"
  brew list pyenv || brew install pyenv
  brew list pyenv-virtualenv || brew install pyenv-virtualenv
  pyenv versions | grep "$(PY_VERSION)" || pyenv install ${PY_VERSION}
  brew list httpie || brew install httpie
  brew list tfenv || brew install tfenv
}

function venvExists() {
  N=1
  if [ "$#" -ne ${N} ]; then
    echo "activateVenv needs ${N} parameter(s)"
    exit 1
  fi
  moduleName=$1
  VENV_NAME="${moduleName}-${PY_VERSION}"
  totalAvailableEnvs=$(pyenv virtualenvs | grep -c "${VENV_NAME}")

  if [[ ${totalAvailableEnvs} -ge 2 ]]; then
    return 0
  else
    return 1
  fi
}

# $# Stores the number of command-line arguments that were passed to the shell program. $? Stores the exit value of the last command that was executed

# "if [$# -ne 0 -a $# -ne 1];" :
# if checks for the condition specified
# ' [ ' and ' ] ' act as short hand notation for test command
# -ne stands for notequal
# $# has the number of arguments passed.
# -a stands for 'AND' operation.
# so in simple english it is :
# "if number of arguments are not equal to 0 and if number of arguments are not equal to 1 get inside the if condition block of code. "

function createNewVenv() {
  N=1
  if [ "$#" -ne ${N} ]; then
    echo "activateVenv needs ${N} parameter(s)"
    exit 1
  fi
  moduleName=$1
  totalFoundFolders=$(ls -d services/*/ | grep -c "${moduleName}")

  if [[ ${totalFoundFolders} -ne 1 ]]; then
    echo "Invalid Module name"
    exit 1
  fi
  VENV_NAME="${moduleName}-${PY_VERSION}"
  echo "${ccso}--> Installing ${VENV_NAME} <-----${ccend}"
  eval "$(pyenv init -)" &&
    eval "$(pyenv virtualenv-init -)" &&
    pyenv virtualenv ${PY_VERSION} "${VENV_NAME}"
}

function activateEnv() {
  # Check if the module name parameter is present
  N=1
  if [ "$#" -ne ${N} ]; then
    echo "activate_venv needs ${N} parameter(s)"
    exit 1
  fi
  moduleName=$1
  VENV_NAME="${moduleName}-${PY_VERSION}"
  VENV_DIR="${PYENV_ROOT}/versions/${VENV_NAME}"
  VENV_EXECUTABLE="${VENV_DIR}/bin/activate"

  moduleBasePath="./services/${moduleName}"

  # Check if VENV directory is available
  if venvExists "$1"; then
    echo "${ccso}--> Activating  ${VENV_NAME} <-----${ccend}"

    # shellcheck disable=SC1090
    source "${VENV_EXECUTABLE}" &&
      pip install -U pip &&
      echo "Using $(which python)" &&
      pip install -r "${moduleBasePath}"/requirements.txt &&
      pip install uvicorn==0.17.6

  else
    echo "${ccso}--> Requested venv ${VENV_DIR} doesn't exist.${ccend}"
    exit 1
  fi
}

function deleteEnv() {
  N=1
  if [ "$#" -ne ${N} ]; then
    echo "delete_venv needs ${N} parameter(s)"
    exit 1
  fi

  moduleName=$1
  VENV_NAME="${moduleName}-${PY_VERSION}"
  VENV_DIR="${PYENV_ROOT}/${VENV_NAME}"
  echo "${ccso}--> Deleting Virtual Environment <-----${ccend}"
  pyenv virtualenv-delete --force "${VENV_NAME}"
}

function test(){
  N=1
  if [ "$#" -ne ${N} ]; then
    echo "delete_venv needs ${N} parameter(s)"
    exit 1
  fi
  if venvExists "$1"; then
    echo "Existing venv found"
  else
    createNewVenv "${moduleName}"
  fi

  moduleName=$1
  # export DB_URI="postgresql://developer:developer@localhost:5432/test_db_utils?connect_timeout=10"
  export DB_URI="sqlite:///database.db"
  export SECRET_KEY="3b7909e3c9914ad1724bacc506ddfa2419516721f13c8e2dfb7c3c447b442008"
  export PYTHONPATH=$(realpath ./services/${moduleName})
  activateEnv "${moduleName}" &&
  pytest -rf -v -p no:warnings \
    --disable-pytest-warnings ./services/${moduleName}/tests


}

function runLocally() {
  # Variables needed for executing apps locally
  export DB_URI="sqlite:///database.db"
  export SECRET_KEY="secretkey"
  export PYTHONPATH="$(pwd)/services/${moduleName}"
  export ES_HOST_NAME="localhost"

  N=1
  if [ "$#" -ne ${N} ]; then
    echo "runModule needs ${N} parameter(s)"
    exit 1
  fi

  moduleName=$1
  VENV_NAME="${moduleName}-${PY_VERSION}"
  executablePath="main:app"

  # shellcheck disable=SC2119
  if venvExists "$1"; then
    echo "Existing venv found"
  else
    createNewVenv "${moduleName}"
  fi

  activateEnv "${moduleName}" &&
    clear &&
    cd ./services/"${moduleName}" &&
    uvicorn --host=0.0.0.0 --port=9558 --workers=1 --limit-concurrency=50 \
      --backlog=100 --use-colors \
      "${executablePath}" --reload
}

function cleanup() {
  # shellcheck disable=SC2012
  rm -rf services/__pycache__
  rm -rf services/alembic/__pycache__
  rm -rf services/alembic/versions/__pycache__
  rm -rf services/alembic/versions/*.py
  # shellcheck disable=SC2012
  for file in $(ls -d services/*/ | cut -f2 -d'/') ; do
    echo "Deleting ${file}"
    deleteEnv "${file}" || true
  done
  # undeploy
  rm -rf .aws-sam || true
  # rm -rf .python-version || true
  find . -name "*.db" -delete
}

function makeMigrations() {
  N=1
  if [ "$#" -ne ${N} ]; then
    echo "makeMigrations needs ${N} parameter(s)"
    exit 1
  fi
  cd ./services/
  migrationName=$1
  alembic revision --autogenerate -m "${migrationName}"
}

function migrate(){
  cd ./services/
  alembic upgrade head      
}
# function deploy() {
#   sam validate -t ${TEMPLATE_FILE_NAME}
#   sam build --template-file=${TEMPLATE_FILE_NAME} --use-container
#   sam package --s3-bucket=${LAMBDA_S3_BUCKET_NAME} --output-template-file=${SAM_TEMPLATE_FILE_NAME} --region="${AWS_DEFAULT_REGION}"
#   sam deploy --template-file=${SAM_TEMPLATE_FILE_NAME} --stack-name=${CF_STACK_NAME}  --region="${AWS_DEFAULT_REGION}" --no-fail-on-empty-changeset --capabilities CAPABILITY_IAM
# }

# function deployLocal(){
#   sam validate -t ${TEMPLATE_FILE_NAME}
#   sam build --template-file=${TEMPLATE_FILE_NAME} --base-dir="${BASE_DIR}" --use-container
#   sam package --s3-bucket=${LAMBDA_S3_BUCKET_NAME} --output-template-file=${SAM_TEMPLATE_FILE_NAME} --region="${AWS_DEFAULT_REGION}"
#   sam local start-api
# }

# function undeploy() {
#     echo "${ccso}--> Deleting AWS Resources <-----${ccend}"
#     #aws cloudformation delete-stack --stack-name ${CF_STACK_NAME}
# }