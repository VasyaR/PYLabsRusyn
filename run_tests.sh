echo "is_testing = True" > config.py
coverage run --source=app -m unittest discover && coverage report -m
