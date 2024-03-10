lint:
	ruff check --select I --fix . && ruff format .

scheduler-db-init:
	cd ./scheduler && PYTHONPATH=.. python cli.py initdb && cd ..

scheduler-db-drop:
	cd ./scheduler && PYTHONPATH=.. python cli.py dropdb && cd ..

checker-db-init:
	cd ./checker && PYTHONPATH=.. python cli.py initdb && cd ..

checker-db-drop:
	cd ./checker && PYTHONPATH=.. python cli.py dropdb && cd ..

run-checker:
	cd ./checker && PYTHONPATH=.. python run.py && cd ..

run-scheduler:
	cd ./scheduler && PYTHONPATH=.. python run.py && cd ..

test-checker:
	cd ./checker && PYTHONPATH=.. python -m pytest && cd ..

test-scheduler:
	cd ./scheduler && PYTHONPATH=.. python -m pytest && cd ..
