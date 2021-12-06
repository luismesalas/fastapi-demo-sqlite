venv:
	python3 -m venv venv
	venv/bin/python3 -m pip install --upgrade pip setuptools
	venv/bin/python3 -m pip install -r requirements-dev.txt

reset_db: venv
	python init_db.py

docker_build:
	docker build -t fastapi-demo-sqlite .

clean:
	rm -rf venv
