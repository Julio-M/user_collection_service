SHELL := /bin/bash
.PHONY: test run deploy deploy-local undeploy cleanup migrations migrate setup-env
.ONESHELL:

guard-%:
	@ if [ "${${*}}" = "" ]; then echo "Environment variable $* not set"; exit 1; fi



# COLOUR FORMATTING
ccend=$(shell tput sgr0)
ccbold=$(shell tput bold)
ccgreen=$(shell tput setaf 2)
ccso=$(shell tput smso)


test-health:
	# make test
	@ source setup.sh ; health

test-func: guard-module
	@ source setup.sh ; activateEnv $(module)

format:
	#format code
	black services/

run: guard-module
	# make run
	@ source setup.sh ; runLocally $(module)

deploy:
	# make deploy
	# @ source deploy.sh ; deploy

undeploy:
	# make undeploy
	# @ source deploy.sh ; undeploy

deploy-local:
	# make deploy-local
	# @ source deploy.sh ; deployLocal

test: guard-module
	# make test
	@ . setup.sh ; test $(module)

cleanup:
	# make cleanup: guard-module
	@ echo "$(ccso)--> Cleaning up all auxiliary files $(ccend)"
	@ source setup.sh ; cleanup $(module)

migrations: guard-name
	# make migrations
	@ echo "$(ccso)--> Creating migrations $(ccend)"
	@ source setup.sh ; makeMigrations ${name}

migrate:
	# make migrate
	@ echo "$(ccso)--> Migrating $(ccend)"
	@ source setup.sh ; migrate

setup-env: guard-module 
	# make setup enviroment
	@ echo "$(ccso)--> setting up $(ccend)"
	@ source setup.sh ; activateEnv $(module)

deploy-ready:
	# make migrate
	@ echo "$(ccso)--> Deploying $(ccend)"
	@ source setup.sh ; deployReady
