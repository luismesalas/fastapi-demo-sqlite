venv:
	python3 -m venv venv
	venv/bin/python3 -m pip install --upgrade pip setuptools
	venv/bin/python3 -m pip install -r requirements-dev.txt

reset_db: venv
	python init_db.py

docker_build:
	docker build -t fastapi-demo-sqlite .

docker_start:
	docker run --rm --name=fastapi-demo-sqlite -p 5000:5000 fastapi-demo-sqlite

docker_stop:
	docker stop fastapi-demo-sqlite

clean:
	rm -rf venv
