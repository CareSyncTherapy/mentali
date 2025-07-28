start:
	docker-compose up --build

test:
	docker-compose exec backend pytest 