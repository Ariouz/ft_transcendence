DEFAULT_LANGUAGE=en

SERVICES := api_gateway users_service i18n_service websocket_server
LIBS := libs/ft_requests libs/ft_i18n
PYTHON_VERSION := python3.12
VENV_PATH := .venv/lib/$(PYTHON_VERSION)/site-packages

all: update_libs up-build

stop:
	@echo "Stopping all running containers..."
	@docker stop $$(docker ps -q)

remove:
	@echo "Removing all containers..."
	@docker rm $$(docker ps -a -q)

clean: stop remove delete_libs
	@echo "All containers have been stopped and removed."

build: update_libs update_i18n
	@echo "Building the Docker image..."
	@docker compose build

up:
	@echo "Starting the Docker containers..."
	@docker compose up

upd:
	@echo "Starting the Docker containers..."
	@docker compose up -d

up-d: upd

buildup: update_libs update_i18n
	@echo "Starting the Docker containers..."
	@docker compose up --build

build-up: buildup
up-build: buildup

buildupd: update_libs update_i18n
	@echo "Starting the Docker containers..."
	@docker compose up --build -d

build-up-d: buildupd

down:
	@echo "Stopping the Docker containers..."
	@docker compose down

logs:
	@echo "Showing logs of Docker containers..."
	@docker compose logs -f

clean-images:
	@echo "Removing all dangling images..."
	@docker rmi $$(docker images -f "dangling=true" -q)

fclean-images:
	@echo "Removing all images..."
	@docker rmi $$(docker images -q) -f

clean-volumes:
	@echo "Removing all dangling volumes..."
	@docker volume rm $$(docker volume ls -qf dangling=true)

prune:
	@echo "Pruning all unused Docker data..."
	@docker system prune -f

restart: down up
	@echo "Docker containers have been restarted."

update_libs: delete_libs deploy_libs

deploy_libs:
	@echo "Starting libs_builder container..." ; echo
	@docker compose up libs_builder ; echo
	@echo "libs_builder container finished." ; echo
	@echo "Running deployment script..." ; echo
	@./libs/deploy_libs.sh ; echo
	@echo "Deployment completed successfully."


delete_libs: delete_libs_virtual_environments
	@echo "Running cleanup script..." ; echo
	@./libs/cleanup_libs.sh ; echo
	@echo "Cleanup script completed successfully." ; echo
	@echo "Starting libs_cleaner container..." ; echo
	@docker compose up libs_cleaner ; echo
	@echo "libs_cleaner container finished."

cleanup_libs: delete_libs

delete_libs_virtual_environments:
	@echo "Removing virtual environments from backends..."
	@for service in $(SERVICES); do \
		echo "Deleting libraries from $$service virtual environment..."; \
		for lib in $(LIBS); do \
			echo "Removing $$lib from $$service..."; \
			sudo rm -rf $$service/$(VENV_PATH)/$$lib; \
			sudo rm -rf $$service/$(VENV_PATH)/$${lib}-0.1.dist-info; \
		done; \
	done

LOCALES_PATH=i18n_service/i18n_service/i18n_service_app/locales
TO_SET_LOCALE_PATHS=website/src/assets/locale/ \
					libs/ft_i18n/ft_i18n/locale/

update_i18n:
	for path in ${TO_SET_LOCALE_PATHS}; do \
		mkdir -p $$path; \
		cp -f ${LOCALES_PATH}/${DEFAULT_LANGUAGE}.json $$path; \
	done

install_wheel:
	python3 -m pip install wheel

#########################################
############### TO REMOVE ###############
#########################################
DB_NAME=postgres
DB_USER=postgres
CONTAINER_NAME="users_service-database"

insert_test_user:
	make insert_user username=testuser email=testuser@example.com password=testuserpassword

insert_user:
	@if [ -z "$(username)" ]; then \
		echo "Usage: make insert_user username=<username> [email=<email>] [password=<password>]"; \
		exit 1; \
	fi; \
	demail=$(email); \
	if [ -z "$${demail}" ]; then \
		demail="$(username)@example.com"; \
	fi; \
	dpassword=$(password); \
	if [ -z "$${dpassword}" ]; then \
		dpassword="$$(openssl rand -base64 12)"; \
	fi; \
	docker exec -i $(CONTAINER_NAME) psql -U $(DB_USER) -d $(DB_NAME) -c "INSERT INTO users_service_app_user (username, email, password) VALUES ('$(username)', '$${demail}', '$${dpassword}');"; \
	echo "User $(username) with email $${demail} and password $${dpassword} has been inserted."

view_users:
	docker exec -i $(CONTAINER_NAME) psql -U $(DB_USER) -d $(DB_NAME) -c "SELECT * FROM users_service_app_user;"

clear_users:
	docker exec -i $(CONTAINER_NAME) psql -U $(DB_USER) -d $(DB_NAME) -c "DELETE FROM users_service_app_user;"

list_tables:
	docker exec -i $(CONTAINER_NAME) psql -U $(DB_USER) -d $(DB_NAME) -c "\dt"
#########################################
############# end TO REMOVE #############
#########################################


structure:
	@if [ -z "$(path)" ]; then \
		to_find_path="."; \
	else \
		to_find_path="$(path)"; \
	fi; \
	echo "Project structure for path: $${to_find_path}"; \
	find $${to_find_path} -path $${to_find_path}/.git -prune -o \
				-name venv -prune -o \
				-name .venv -prune -o \
				-name __pycache__ -prune -o \
				-name __init__.py -prune -o \
				-name migrations -prune -o \
				-name .idea -prune -o \
		-print | sed -e "s/[^-][^\/]*\// |/g" -e "s/|\([^ ]\)/|-\1/"


.PHONY: stop remove clean \
		build up upd up-d buildup build-up up-build buildupd build-up-d \
		down logs clean-images fclean-images clean-volumes prune restart \
		update_libs deploy_libs delete_libs cleanup_libs delete_libs_virtual_environments \
		update_i18n \
		insert_user insert_test_user view_users clear_users list_tables \
		structure
