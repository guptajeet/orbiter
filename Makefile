.PHONY: install run-backend run-dashboard run-worker run-beat docker-up docker-down test lint clean

install:
	cd backend && pip install -r requirements.txt
	cd dashboard && npm install

run-backend:
	cd backend && python main.py

run-dashboard:
	cd dashboard && npm run dev

run-worker:
	cd backend && celery -A backend.tasks.celery_app worker --loglevel=info

run-beat:
	cd backend && celery -A backend.tasks.celery_app beat --loglevel=info

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

test:
	pytest tests/ -v --cov=backend

lint:
	cd backend && python -m py_compile main.py
	cd dashboard && npm run lint

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -f backend/orbiter.db
