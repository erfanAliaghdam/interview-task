## delete migrations
> find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

> find . -path "*/migrations/*.pyc"  -delete

## run project by docker-compose
> docker-compose up --build -d

## generate dev seeds
step 1 :
> docker-compose run backend sh

step 2:
> python manage.py generate_dev_seeds

note: you can use -y for answering all questions yes by default...

## test coverage
> coverage run manage.py test & coverage report -m

## development users

superuser :
> email: superuser@example.com
> password: DefaultPassword

client user (Support Group):
> email: client@example.com
> password: DefaultPassword
