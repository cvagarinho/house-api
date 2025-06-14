.PHONY: install test up down logs build status check-api requirements clean rebuild-clean rabbitmq-ui worker-logs worker-restart format lint

install:
	pip install -r requirements.txt

up:
	docker-compose --env-file .env.local up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	pytest tests -v

build:
	docker-compose --env-file .env.local up -d --build

status:
	docker ps | grep house

check-api:
	docker logs house_api -f

requirements:
	pip freeze > requirements.txt

clean:
	docker-compose down -v
	docker system prune -f
	docker-compose --env-file .env.local up -d --build --force-recreate

rebuild-clean:
	$(MAKE) down
	$(MAKE) clean

rabbitmq-ui:
	@echo "RabbitMQ UI available at http://localhost:15672"

service-logs:
	docker logs $(service) -f

format:
	isort .
	black .

lint:
	pyflakes ./app ./tests


