run:
	docker compose up --build

down:
	docker compose down

fmt:
	black services/rasa/actions actions || true
