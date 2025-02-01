DEFAULT_LANGUAGE=en

all: ssl_cert update_libs up-build

ci-github-actions: ssl_cert update_libs build-up-d

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

update_libs: deploy_libs
# todo voir pour remettre delete_libs en premiere dependance


ssl_cert:
	@mkdir -p ssl_certs
# @chmod 777 -R ssl_certs
	@echo "Generating new certificates..."
	@echo "[req]" > tmp_openssl.cnf
	@echo "distinguished_name = req" >> tmp_openssl.cnf
	@echo "[SAN]" >> tmp_openssl.cnf
	@echo "subjectAltName = DNS:localhost,DNS:users-service,DNS:pong-service" >> tmp_openssl.cnf
	
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
		-keyout ./ssl_certs/selfsigned.key -out ./ssl_certs/selfsigned.crt \
		-subj "/C=FR/ST=State/L=City/O=Organization/OU=Department/CN=localhost" \
		-extensions SAN \
		-config tmp_openssl.cnf
	rm -f tmp_openssl.cnf
# @chmod 777 -R ssl_certs


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

SERVICES := users_service pong_service i18n_service websocket_server
PYTHON_VERSION := python3.12
VENV_PATH := .venv/lib/$(PYTHON_VERSION)/site-packages
LIBS := ft_requests ft_i18n
delete_libs_virtual_environments:
	@echo "Removing virtual environments from backends..."
	@for service in $(SERVICES); do \
		echo "Deleting libraries from $$service virtual environment..."; \
		for lib in $(LIBS); do \
			echo "Removing $$lib from $$service..."; \
			echo "$$service/$(VENV_PATH)/$$lib" \
			echo "$$service/$(VENV_PATH)/$${lib}-0.1.dist-info" \
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


.PHONY: all ci-github-actions stop remove clean \
		build up upd up-d buildup build-up up-build buildupd build-up-d \
		down logs clean-images fclean-images clean-volumes prune restart \
		update_libs deploy_libs delete_libs cleanup_libs delete_libs_virtual_environments \
		update_i18n \
		insert_user insert_test_user view_users clear_users list_tables \
		structure
