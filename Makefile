# makemigrations

mm :
	python manage.py makemigrations

# migrate

mg: 
	python manage.py migrate

# run local server

run :
	python manage.py runserver

# update migrations
requirements: 
	rm requirements.txt
	pip freeze > requirements.txt

# run all tests
test:
	python manage.py test

# run functional tests
func:
	python manage.py test functional_tests

# run test for app "main"
test_main: 
	python manage.py test main

# run test for app "users"
test_users:
	python manage.py test users