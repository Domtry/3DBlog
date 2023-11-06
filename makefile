env_file:
	pip freeze > requirements.txt

clean_env:
	pip uninstall -r requirements.txt -y
