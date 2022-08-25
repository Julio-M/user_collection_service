.PHONY: test run deploy deploy-local undeploy cleanup
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
	@ source deploy.sh ; health

format:
	#format code
	black services/

run: guard-module
	# make run
	@ source deploy.sh ; runLocally $(module)

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
	@ . deploy.sh ; test $(module)

cleanup:
	# make cleanup
	@ echo "$(ccso)--> Cleaning up all auxiliary files $(ccend)"
	@ source deploy.sh ; cleanup

migrations: guard-module guard-name
	# make migrations
	@ echo "$(ccso)--> Creating migrations $(ccend)"
	@ source deploy.sh ; makeMigrations $(module) ${name}

migrate:
	# migrate
	@ echo "$(ccso)--> Migrating $(ccend)"
	@ source deploy.sh ; migrate

setup-env:
	# migrate
	@ echo "$(ccso)--> setting up $(ccend)"
	@ source deploy.sh ; setupEnvironment

