env_file:
	pip freeze > requirements.txt

clean_env:
	pip uninstall -r requirements.txt -y

init:
	python3 -m venv env && source env/bin/activate
	pip install -r requirements.txt

