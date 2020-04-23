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
